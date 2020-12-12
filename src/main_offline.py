import Data.load_data as dat
import Models.statistics as man
import Models.predictions as pred
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #data = dat.load_invoices_from_nif_costs("1234")
    #timedelta = 'D'

    
    #res = man.n_invoices_per_category_per_delta(data, timedelta, False)
    
    #json_data = res.to_json(orient='records')
    #print(json_data)

    nif="1234"
    delta="M"

   # data_costs = dat.load_invoices_from_nif_costs(nif)
    #data_earns = dat.load_invoices_from_nif_incomes(nif)

    data = pd.read_csv('../testing_datasets/accounts_payable_v2_complete_adapted.csv')
    model, forecast = pred.forecast_growth_simple(data,365)
    fig = model.plot(forecast)
    plt.show()

    #json_format = {
    #    'dates': res1['dates'].tolist(),
    #    'costs_values': res1['values'].tolist(),
    #    'gains_values': res2['values'].tolist(),
    #}

    #print(json_format)
