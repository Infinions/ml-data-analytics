import pandas as pd

"""
DELTA EXPLANATION
M -> monthly data
Q -> quarterly data
Y -> yearly data
2BQS -> biannual data
"""

def invoices_sum_per_timedelta(data, delta):
    tmp_data = data.copy()
    tmp_data = tmp_data[['total_value', 'doc_emission_date']]
    tmp_data = tmp_data.groupby([pd.Grouper(key="doc_emission_date", freq=delta)])['total_value'].sum()
    return tmp_data


# REDUNDANTE
def n_invoices_per_category(data):
    tmp_data = data.copy()
    tmp_data = tmp_data[['category','id']]
    tmp_data = tmp_data.groupby('category').count()
    tmp_data.columns = ['n_invoices']
    return tmp_data


def n_invoices_per_category_per_delta(data, delta, count=True):
    tmp_data = data.copy()
    tmp_data = tmp_data[['category','doc_emission_date']]
    if count:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="doc_emission_date", freq=delta),'category'])['category'].count())
    else:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="doc_emission_date", freq=delta),'category'])['category'].sum())
    tmp_data.columns = ['n_invoices']
    return tmp_data


def n_invoices_per_client_per_delta(data, delta, count=True):
    tmp_data = data.copy()
    tmp_data = tmp_data[['company_seller_name','doc_emission_date']]
    if count:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="doc_emission_date", freq=delta),'company_seller_name'])['company_seller_name'].count())
    else:
        tmp_data = pd.DataFrame(tmp_data.groupby([pd.Grouper(key="doc_emission_date", freq=delta),'company_seller_name'])['company_seller_name'].sum())
    tmp_data.columns = ['n_invoices']
    return tmp_data
