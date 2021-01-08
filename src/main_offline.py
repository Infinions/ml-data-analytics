import Data.load_data as dat
import Models.statistics as man
import Models.predictions as pred
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = dat.load_all_costs_from_nif("1234")
    print(data)
    #timedelta = 'D'

    
    #res = man.n_invoices_per_category_per_delta(data, timedelta, False)
    
    #json_data = res.to_json(orient='records')
    #print(json_data)

    #nif="1234"
    #delta="D"

    #tmp = pred.forecast_growth(data,15, delta, 'simple')
    #print(tmp)

    #res1 = man.invoices_per_client_per_delta(data, delta, None, True)
    #res1 = res1.set_index(['date','company_seller_name'])
    #print(res1)
    #tmp_data = dat.fill_gap_dates(res1)
    #print(tmp_data)
    #tmp_data = tmp_data.reset_index()
    #tmp_data = tmp_data.rename(columns={'level_0': 'date'})
    
    #vals = {}

    #for r in tmp_data['company_seller_name'].unique():
    #    vals[r] = tmp_data[tmp_data['company_seller_name'] == r]['total_value'].values

    #print(vals)



    #cats = tmp_data['company_seller_name'].values.tolist()
    #print(len(cats))
    #vals = tmp_data['total_value'].values.tolist()
    #print(len(vals))


   # data_costs = dat.load_invoices_from_nif_costs(nif)
    #data_earns = dat.load_invoices_from_nif_incomes(nif)

    #data = pd.read_csv('../testing_datasets/accounts_payable_v2_complete_adapted.csv')
    #model, forecast = pred.forecast_growth_simple(data,365)
    #fig = model.plot(forecast)
    #plt.show()

    """ data_costs = pd.read_csv('../testing_datasets/accounts_payable_v2_complete_adapted.csv')
    data_costs = data_costs.rename(columns={'doc_emission_date': 'date'})
    data_costs['date'] = pd.to_datetime(data_costs.date)

    res1 = man.invoices_sum_per_timedelta(data_costs, delta)
    res1.columns = ['dates','values']

    # Make both dataframes with the same timeline to safely concat after

    window_start = "2010-5-15"
    window_end = "2015-5-15"

    window_start = pd.to_datetime(window_start)
    window_end   = pd.to_datetime(window_end)

    res1 = res1[(res1['dates'] >= window_start) & (res1['dates'] <= window_end)]

 """
    #json_format = {
    #    'dates': res1['dates'].tolist(),
    #    'costs_values': res1['values'].tolist(),
    #    'gains_values': res2['values'].tolist(),
    #}

    #print(json_format)
