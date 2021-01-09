from graphene import ObjectType, Schema, Field, List, String, Boolean, JSONString, Int
import pandas as pd
import time
import json
import os
import Models.statistics as data_manipulation
import Models.predictions as data_predictors
import Data.load_data as load_data
from Models.recomendation_system import RecommendationSystem
from BD.mongo_controller import MongoController


export_type = 'columns'
mongo_string = os.getenv('DB_ANALYTICS') if os.getenv('DB_ANALYTICS') != None else None

db_controller = MongoController(mongo_string)


class RootQuery(ObjectType):
    class Meta:
        description = "Query manager for retrieving chart data and other types of AI augmentation."

    sum_invoices = JSONString(
        description  = "Sum of invoices from a user.",
        nif          = String(required=True, description="NIF of the user."),
        delta        = String(default_value='D', description="Timedelta used for grouping of data."),
        window_start = String(default_value='', description="Start date for the window of data."),
        window_end   = String(default_value='', description="End date for the window of data.")
    )
    n_invoices_category = JSONString(
        description  = "Count or sum of invoices from a user relative to categorie(s).",
        nif          = String(required=True, description="NIF of the user."),
        delta        = String(default_value='D', description="Timedelta used for grouping of data."),
        is_count     = Boolean(default_value=True, description="If count instead of sum is desired."),
        category     = String(default_value="", description="Specific category name to relate data to."),
        window_start = String(default_value='', description="Start date for the window of data."),
        window_end   = String(default_value='', description="End date for the window of data.")
    )
    n_invoices_client = JSONString(
        description  = "Count or sum of invoices from a user relative to client(s).",
        nif          = String(required=True, description="NIF of the user."),
        delta        = String(default_value='D', description="Timedelta used for grouping of data."),
        is_count     = Boolean(default_value=True, description="If count instead of sum is desired."),
        client_nif   = String(default_value="", description="Specific client NIF to relate data to."),
        window_start = String(default_value='', description="Start date for the window of data."),
        window_end   = String(default_value='', description="End date for the window of data.")
    )
    predict_future = JSONString(
        description  = "Predict the future of the costs, based on a simpler but quicker approach.",
        nif          = String(required=True, description="NIF of the user."),
        time         = Int(required=True, description="Amount of time to predict the future."),
        delta        = String(default_value='D', description="Timedelta used for grouping of data."),
        method       = String(default_value='simple', description="Method to create prediction. Simple means faster but less accurate.")
    )
    categorize_invoices = JSONString(
        description = "Recommends category for multiple invoices.",
        invoices    = JSONString(required=True, description="Invoices to be categorized.")
    )

    @staticmethod
    def resolve_categorize_invoices(parent, info, invoices):
        inv_dt = pd.DataFrame.from_dict(invoices['list'], orient='columns')
        inv_dt = inv_dt.rename(columns={'doc_emission_date': 'date'})
        inv_dt['nif'] = inv_dt.nif.astype(str)
        recommender = RecommendationSystem(inv_dt['nif'][0], db_controller)

        if recommender.check_existing_model():
            recommender.load_model()
        else:
            data = load_data.load_invoices_from_nif_costs(inv_dt['nif'][0])
            if data.empty:
                return []
            recommender.prepare_data(data)
            recommender.train_model()
            recommender.save_model()

        categories = recommender.recommend_category(inv_dt)
        
        results = {}
        for i in range(len(categories)):
            results[i] = int(categories[i])

        return results

    @staticmethod
    def resolve_predict_future(parent, info, nif, time, delta, method):
        data_costs = load_data.load_all_costs_from_nif(nif)

        res1 = data_predictors.forecast_growth(data_costs, time, delta, method)

        if res1.empty:
            dates = []
        else:
            dates = res1['dates'].dt.strftime('%Y-%m-%d').tolist()

        json_format = {
            'dates': dates,
            'total_value': res1['total_value'].tolist(),
        }        
        return json_format

    @staticmethod
    def resolve_n_invoices_client(parent, info, nif, delta, is_count, client_nif, window_start, window_end):
        if client_nif == "":
            client_nif = None

        data_costs = load_data.load_all_costs_from_nif(nif)

        res1 = data_manipulation.invoices_per_client_per_delta(data_costs, delta, client_nif, is_count)
        res1 = load_data.filter_by_date(res1, 'dates', window_start, window_end)

        res1 = res1.set_index(['dates','company_seller_name'])
        res1 = load_data.fill_gap_dates(res1)
        res1 = res1.reset_index() 
        res1 = res1.rename(columns={'level_0': 'dates'})

        if res1.empty:
            dates = []
        else:
            dates = res1['dates'].dt.strftime('%Y-%m-%d').tolist()

        json_format = {
            'dates': dates,
            'companies': {}
        }

        for r in res1['company_seller_name'].unique():
            json_format['companies'][r] = res1[res1['company_seller_name'] == r]['total_value'].tolist()

        return json_format

    @staticmethod
    def resolve_n_invoices_category(parent, info, nif, delta, is_count, category, window_start, window_end):
        if category == "":
            category = None
        
        data_costs = load_data.load_all_costs_from_nif(nif)

        res1 = data_manipulation.invoices_per_category_per_delta(data_costs, delta, category, is_count)
        res1 = load_data.filter_by_date(res1, 'dates', window_start, window_end)

        res1 = res1.set_index(['dates','category'])
        res1 = load_data.fill_gap_dates(res1)
        res1 = res1.reset_index() 
        res1 = res1.rename(columns={'level_0': 'dates'})

        if res1.empty:
            dates = []
        else:
            dates = res1['dates'].dt.strftime('%Y-%m-%d').tolist()

        json_format = {
            'dates': dates,
            'categories': {}
        }

        for r in res1['category'].unique():
            json_format['categories'][r] = res1[res1['category'] == r]['total_value'].tolist()

        return json_format

    @staticmethod
    def resolve_sum_invoices(parent, info, nif, delta, window_start, window_end):
        data_costs = load_data.load_all_costs_from_nif(nif)
        data_earns = load_data.load_invoices_from_nif_incomes(nif)

        res1 = data_manipulation.invoices_sum_per_timedelta(data_costs, delta)
        res1.columns = ['dates','values']
        res2 = data_manipulation.invoices_sum_per_timedelta(data_earns, delta)
        res2.columns = ['dates','values']

        # Make both dataframes with the same timeline to safely concat after
        res1, res2 = load_data.adjust_datasets_length(res1, res2)

        # After making same length, both need to be readjusted relative to delta
        if delta != 'D':
            res1 = res1.groupby([pd.Grouper(key="dates", freq=delta)])['values'].sum()
            res1 = res1.reset_index()
            res2 = res2.groupby([pd.Grouper(key="dates", freq=delta)])['values'].sum()
            res2 = res2.reset_index()

        res1 = load_data.filter_by_date(res1, 'dates', window_start, window_end)
        res2 = load_data.filter_by_date(res2, 'dates', window_start, window_end)

        if res1.empty and res2.empty:
            dates = []
        else:
            dates = res1['dates'].dt.strftime('%Y-%m-%d').tolist()

        json_format = {
            'dates': dates,
            'costs_values': res1['values'].tolist(),
            'gains_values': res2['values'].tolist(),
        }        
        return json_format

