import Data.load_data as dat
import Models.manipulation as man

if __name__ == "__main__":
    data = dat.load_invoices_from_nif_costs("1234")
    print(man.n_invoices_per_client_per_delta(data, 'Q'))