import psycopg2 as pg
import pandas as pd
import pandas.io.sql as psql
import numpy as np
 
# get connected to the database
connection = pg.connect(dbname="infin_dev", user="infin", password="infin",
                        host="localhost", port="5432")  # Change to read from configuration file


#Represents a COST
def load_invoices_from_nif_costs(nif):
    query = "SELECT invoices.*, cn.nif as company_nif, cn.name as company_name, csn.nif as company_seller_nif, csn.name as company_seller_name, cat.name as category\
                FROM invoices\
             INNER JOIN companies as cn ON invoices.company_id=cn.id\
             INNER JOIN companies as csn ON invoices.company_seller_id=csn.id\
             LEFT JOIN categories as cat ON invoices.category_id=cat.id\
                WHERE cn.nif='"+nif+"'"

    dataframe = psql.read_sql(query, connection)
    pd.set_option('display.expand_frame_repr', False)
    dataframe.drop(columns=['doc_hash', 'inserted_at', 'updated_at'], inplace=True)
    dataframe['doc_emission_date'] = pd.to_datetime(dataframe.doc_emission_date)
    return dataframe

#Represents an EARNING
def load_invoices_from_nif_earnings(nif):
   query = "SELECT invoices.*, cn.nif as company_nif, csn.nif as company_seller_nif, cat.name as category\
               FROM invoices\
            INNER JOIN companies as cn ON invoices.company_id=cn.id\
            INNER JOIN companies as csn ON invoices.company_seller_id=csn.id\
            LEFT JOIN categories as cat ON invoices.category_id=cat.id\
               WHERE csn.nif='"+nif+"'"

   dataframe = psql.read_sql(query, connection)
   pd.set_option('display.expand_frame_repr', False)
   dataframe.drop(columns=['doc_hash', 'inserted_at', 'updated_at'], inplace=True)
   dataframe['doc_emission_date'] = pd.to_datetime(dataframe.doc_emission_date)      
   return dataframe


def adjust_datasets_length(costs, gains):
   if costs.empty and gains.empty:
      return costs, gains

   sd_c = costs.head(1)['dates'] if not costs.empty else gains.head(1)['dates']
   sd_g = gains.head(1)['dates'] if not gains.empty else costs.head(1)['dates']

   ed_c = costs.tail(1)['dates'] if not costs.empty else gains.tail(1)['dates']
   ed_g = gains.tail(1)['dates'] if not gains.empty else costs.tail(1)['dates']

   if (sd_c > sd_g).bool():
      start_date = sd_g
   else:
      start_date = sd_c

   if (ed_c > ed_g).bool():
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

   costs = costs.set_index('dates')
   gains = gains.set_index('dates')

   costs_new = costs_new.combine_first(costs).fillna(0, downcast='infer')
   gains_new = gains_new.combine_first(gains).fillna(0, downcast='infer')

   costs_new.reset_index(inplace=True)
   gains_new.reset_index(inplace=True)

   return costs_new, gains_new


'''
def load_and_prepare_data(nif):
   data_costs = load_invoices_from_nif_costs(nif)
   data_earns = load_invoices_from_nif_earnings(nif)

   data_costs['doc_emission_date'] = pd.to_datetime(data_costs['doc_emission_date'])
   data_earns['doc_emission_date'] = pd.to_datetime(data_earns['doc_emission_date'])

   data_costs = data_costs.set_index('doc_emission_date')
   data_earns = data_earns.set_index('doc_emission_date')

   final_data = pd.concat([data_costs, data_earns], axis=1)

   final_data = final_data.resample('D').pad()     # TODO Better handling for missing data
   print(final_data.head())
   final_data = final_data.reset_index()

   return final_data
'''