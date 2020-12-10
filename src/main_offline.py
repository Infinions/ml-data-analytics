import Data.load_data as dat
import Models.statistics as man
#import Models.predictions as pred
import pandas as pd
import numpy as np

if __name__ == "__main__":
    #data = dat.load_invoices_from_nif_costs("1234")
    #timedelta = 'D'
    #data = pd.read_csv('../testing_datasets/accounts_payable_v2_complete_adapted.csv')
    #pred.forecast_growth_simple(data,365,timedelta)
    
    #res = man.n_invoices_per_category_per_delta(data, timedelta, False)
    
    #json_data = res.to_json(orient='records')
    #print(json_data)

    nif="1234"
    delta="M"

    data_costs = dat.load_invoices_from_nif_costs(nif)
    data_earns = dat.load_invoices_from_nif_incomes(nif)

    #print(data_earns)

    res1 = man.invoices_sum_per_timedelta(data_costs, delta)
    res1.columns = ['dates','values']
    res2 = man.invoices_sum_per_timedelta(data_earns, delta)
    res2.columns = ['dates','values']

    #print(res1)
    #print(res2)

    res1, res2 = dat.adjust_datasets_length(res1, res2)
    
    print(res1)

    print(res2)

    #res1['dates'] = res1['dates'].dt.strftime('%Y-%m-%d')
    #res2['dates'] = res2['dates'].dt.strftime('%Y-%m-%d')


    #json_format = {
    #    'dates': res1['dates'].tolist(),
    #    'costs_values': res1['values'].tolist(),
    #    'gains_values': res2['values'].tolist(),
    #}

    #print(json_format)
