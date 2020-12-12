import psycopg2 as pg
import pandas as pd
import pandas.io.sql as psql
import numpy as np
 
MIN_INVOICES_PER_MONTH = 5


# connection to the database
connection = pg.connect(dbname="infin_dev", user="infin", password="infin",
                        host="localhost", port="5432")  # Change to read from configuration file


#Represents a COST
def load_invoices_from_nif_costs(nif):
   """Load invoices from database by nif, by costs
   Args:
      nif: String, nif of the user.
   """
   
   query = "SELECT invoices.*, cn.nif as company_nif, cn.name as company_name, csn.nif as company_seller_nif, csn.name as company_seller_name, cat.name as category\
               FROM invoices\
            INNER JOIN companies as cn ON invoices.company_id=cn.id\
            INNER JOIN companies as csn ON invoices.company_seller_id=csn.id\
            LEFT JOIN categories as cat ON invoices.category_id=cat.id\
               WHERE cn.nif='"+nif+"'"

   dataframe = psql.read_sql(query, connection)
   dataframe.drop(columns=['doc_hash', 'inserted_at', 'updated_at'], inplace=True)
   dataframe['doc_emission_date'] = pd.to_datetime(dataframe.doc_emission_date)

   dataframe = dataframe.rename(columns={'doc_emission_date': 'date'})
   return dataframe

#Represents an INCOME
def load_invoices_from_nif_incomes(nif):
   """Load invoices from database by nif, by incomes
   Args:
      nif: String, nif of the user.
    """

   query = "SELECT incomes.value, incomes.date , incomes.description\
               FROM incomes\
            INNER JOIN companies as cn ON incomes.company_id=cn.id\
               WHERE cn.nif='"+nif+"'"

   dataframe = psql.read_sql(query, connection)
   dataframe['date'] = pd.to_datetime(dataframe.date) 
   dataframe.columns = ['total_value','date','description']    
   return dataframe


def adjust_datasets_length(costs, gains):
   """Adjust both datasets so they can have equal date lenghts
   Args:
      costs: Dataframe, costs data.
      gains: Dataframe, gains data.
   """

   if costs.empty and gains.empty:
      return costs, gains

   costs = costs.set_index('dates')
   gains = gains.set_index('dates')

   sd_c = costs.head(1).index if not costs.empty else gains.head(1).index
   sd_g = gains.head(1).index if not gains.empty else costs.head(1).index

   ed_c = costs.tail(1).index if not costs.empty else gains.tail(1).index
   ed_g = gains.tail(1).index if not gains.empty else costs.tail(1).index

   if (sd_c > sd_g)[0]:
      start_date = sd_g
   else:
      start_date = sd_c

   if (ed_c > ed_g)[0]:
      end_date = ed_c
   else:
      end_date = ed_g

   costs_new = pd.DataFrame(None,
      index=pd.date_range(start_date.values[0], end_date.values[0]),
      columns=['values']
   )
   costs_new.index.name = 'dates'

   gains_new = pd.DataFrame(None, 
      index=pd.date_range(start_date.values[0], end_date.values[0]),
      columns=['values']
   )
   gains_new.index.name = 'dates'

   costs_new = costs_new.combine_first(costs).fillna(0, downcast='infer')
   gains_new = gains_new.combine_first(gains).fillna(0, downcast='infer')

   costs_new.reset_index(inplace=True)
   gains_new.reset_index(inplace=True)

   return costs_new, gains_new


def clean_missing_data(data, ind, val):
   """Clean missing data from a dataset. It also handles outliers.
   Args:
      data: Dataframe, costs data.
      ind: String, date column name.
      val: String, value column name.
   """
   
   clean_data = pd.DataFrame(data.reset_index().groupby([pd.Grouper(key=ind, freq='D')])[val].sum()).reset_index()

   # Set NA to montly data without/low number of invoices (it's best to assume it's missing as opposed to no actual/only some invoices were created)
   tmp_data = pd.DataFrame(data.reset_index().groupby([pd.Grouper(key=ind, freq='M')])[val].count())

   for i, _ in tmp_data[tmp_data[val] < MIN_INVOICES_PER_MONTH].iterrows():
      end_m   = i
      start_m = i.replace(day=1)
      clean_data.loc[(clean_data[ind] >= start_m) & (clean_data[ind] <= end_m),val] = None


   return clean_data   



'''
def load_and_prepare_data(nif):
   data_costs = load_invoices_from_nif_costs(nif)
   data_earns = load_invoices_from_nif_earnings(nif)

   data_costs['doc_emission_date'] = pd.to_datetime(data_costs['doc_emission_date'])
   data_earns['doc_emission_date'] = pd.to_datetime(data_earns['doc_emission_date'])

   data_costs = data_costs.set_index('doc_emission_date')
   data_earns = data_earns.set_index('doc_emission_date')

   final_data = pd.concat([data_costs, data_earns], axis=1)

   final_data = final_data.resample('D').pad()     
   print(final_data.head())
   final_data = final_data.reset_index()

   return final_data
'''