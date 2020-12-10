import pandas as pd

"""
DELTA EXPLANATION
D -> daily data
M -> monthly data
Q -> quarterly data
Y -> yearly data
2BQS -> biannual data

- Must end with reset_index
- Date must be in datetime format
"""

def invoices_sum_per_timedelta(data, delta):
    tmp_data = data.copy()
    tmp_data = tmp_data[['total_value', 'date']]

    tmp_data = tmp_data.groupby([pd.Grouper(key="date", freq=delta)])['total_value'].sum()
    tmp_data = tmp_data.reset_index()
    
    return tmp_data

""" 
# REDUNDANTE
def n_invoices_per_category(data):
    tmp_data = data.copy()
    tmp_data = tmp_data[['category','id']]
    tmp_data = tmp_data.groupby('category').count()
    tmp_data.columns = ['n_invoices']

    tmp_data = tmp_data.reset_index()

    return tmp_data
 """

def invoices_per_category_per_delta(data, delta, category, count):
    tmp_data = data.copy()
    tmp_data = tmp_data[['category','date','total_value']]

    if category is not None:
        tmp_data = tmp_data[tmp_data['category'] == category]

    if count is False:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="date", freq=delta),'category'])['total_value'].sum())
    else:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="date", freq=delta),'category'])['total_value'].count())
        tmp_data.columns = ['total_value']

    tmp_data = tmp_data.reset_index()
    if tmp_data.empty:
        return tmp_data
    
    return tmp_data


def invoices_per_client_per_delta(data, delta, client_nif, count):
    tmp_data = data.copy()
    tmp_data = tmp_data[['company_seller_name','company_seller_nif','date', 'total_value']]

    if client_nif is not None:
        tmp_data = tmp_data[tmp_data['company_seller_nif'] == client_nif]
        tmp_data = tmp_data[['company_seller_name','date', 'total_value']]


    if count is False:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="date", freq=delta),'company_seller_name'])['total_value'].sum())
    else:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="date", freq=delta),'company_seller_name'])['total_value'].count())
        tmp_data.columns = ['total_value']

    tmp_data = tmp_data.reset_index()
    if tmp_data.empty:
        return tmp_data
    
    return tmp_data
