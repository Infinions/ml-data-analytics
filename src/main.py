#import Data.load_data as dat
import Models.statistics as man
import Models.predictions as pred
import pandas as pd

if __name__ == "__main__":
    #data = dat.load_invoices_from_nif_costs("1234")
    timedelta = 'D'
    data = pd.read_csv('../testing_datasets/accounts_payable_v2_complete_adapted.csv')
    pred.forecast_growth_simple(data,365,timedelta)
    
    #res = man.n_invoices_per_category_per_delta(data, timedelta, False)
    
    #json_data = res.to_json(orient='records')
    #print(json_data)
