from graphene import ObjectType, Schema, Field, List, String, Boolean, JSONString, Int
import pandas as pd
import Models.statistics as data_manipulation
import Models.predictions as data_predictors
import json
import Data.load_data as load_data
import time

export_type = 'columns'


class RootQuery(ObjectType):
    class Meta:
        description = "Query manager for retreiving chart data."

    sum_invoices = JSONString(
        description = "Sum of invoices from a user.",
        nif         = String(required=True),
        delta       = String(default_value='D'),
        window_start      = String(default_value=''),
        window_end        = String(default_value='')
    )
    n_invoices_category = JSONString(
        description = "Count or sum of invoices from a user relative to categorie(s).",
        nif         = String(required=True),
        delta       = String(default_value='M'),
        is_count    = Boolean(default_value=True),
        category    = String(default_value=""),
        window_start = String(default_value=''),
        window_end   = String(default_value='')
    )
    n_invoices_client = JSONString(
        description  = "Count or sum of invoices from a user relative to client(s).",
        nif          = String(required=True),
        delta        = String(default_value='M'),
        is_count     = Boolean(default_value=True),
        client_nif   = String(default_value=""),
        window_start = String(default_value=''),
        window_end   = String(default_value='')
    )
    predict_future = JSONString(
        description  = "Predict the future of the costs, based on a simpler but quicker approach.",
        nif          = String(required=True),
        time         = Int(required=True),
        delta        = String(default_value='M'),
        method       = String(default_value='simple')
    )

    @staticmethod
    def resolve_predict_future(parent, info, nif, time, delta, method):
        data_costs = load_data.load_invoices_from_nif_costs(nif)

        res1 = data_predictors.forecast_growth(data_costs, time, delta, method)

        json_format = {
            'dates': res1['date'].dt.strftime('%Y-%m-%d').tolist(),
            'total_value': res1['total_value'].tolist(),
        }        
        return json_format

    @staticmethod
    def resolve_n_invoices_client(parent, info, nif, delta, is_count, client_nif, window_start, window_end):
        if client_nif == "":
            client_nif = None

        data_costs = load_data.load_invoices_from_nif_costs(nif)

        res1 = data_manipulation.invoices_per_client_per_delta(data_costs, delta, client_nif, is_count)
        res1 = load_data.filter_by_date(res1, 'date', window_start, window_end)

        res1 = res1.set_index(['date','company_seller_name'])
        res1 = load_data.fill_gap_dates(res1)
        res1 = res1.reset_index() 
        res1 = res1.rename(columns={'level_0': 'date'})

        json_format = {
            'dates': res1['date'].dt.strftime('%Y-%m-%d').unique().tolist(),
            'companies': {}
        }

        for r in res1['company_seller_name'].unique():
            json_format['companies'][r] = res1[res1['company_seller_name'] == r]['total_value'].tolist()

        return json_format

    @staticmethod
    def resolve_n_invoices_category(parent, info, nif, delta, is_count, category, window_start, window_end):
        if category == "":
            category = None
        
        data_costs = load_data.load_invoices_from_nif_costs(nif)

        res1 = data_manipulation.invoices_per_category_per_delta(data_costs, delta, category, is_count)
        res1 = load_data.filter_by_date(res1, 'date', window_start, window_end)

        res1 = res1.set_index(['date','category'])
        res1 = load_data.fill_gap_dates(res1)
        res1 = res1.reset_index() 
        res1 = res1.rename(columns={'level_0': 'date'})

        json_format = {
            'dates': res1['date'].dt.strftime('%Y-%m-%d').unique().tolist(),
            'categories': {}
        }

        for r in res1['category'].unique():
            json_format['categories'][r] = res1[res1['category'] == r]['total_value'].tolist()

        return json_format

    @staticmethod
    def resolve_sum_invoices(parent, info, nif, delta, window_start, window_end):
        data_costs = load_data.load_invoices_from_nif_costs(nif)
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

        json_format = {
            'dates': res1['dates'].dt.strftime('%Y-%m-%d').tolist(),
            'costs_values': res1['values'].tolist(),
            'gains_values': res2['values'].tolist(),
        }        
        return json_format

