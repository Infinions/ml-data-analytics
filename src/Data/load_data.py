import psycopg2 as pg
import pandas as pd
import pandas.io.sql as psql
 
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
    dataframe['doc_emission_date'] = pd.to_datetime(dataframe.doc_emission_date)        #Convert data types to datetime
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
    dataframe['doc_emission_date'] = pd.to_datetime(dataframe.doc_emission_date)        #Convert data types to datetime
    return dataframe

