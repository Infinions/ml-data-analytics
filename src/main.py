import Data.load_data as dat
import Models.manipulation as man

if __name__ == "__main__":
    data = dat.load_invoices_from_nif_costs("1234")
    timedelta = 'Q'
    res = man.n_invoices_per_category_per_delta(data, timedelta, False)
    
    json_data = res.to_json(orient='records')
    print(json_data)
