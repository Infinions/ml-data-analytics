from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
import itertools
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

def __prepare_data(data):
    pr_data = data[['doc_emission_date','total_value']]
    pr_data.columns = ['ds','y']
    pr_data['ds'] = pd.to_datetime(pr_data['ds'])

    pr_data = pr_data.set_index('ds')
    pr_data = pr_data.resample('D').sum().fillna(0)     # TODO Better handling for missing data
    pr_data = pr_data.reset_index()

    return pr_data


def __calculate_best_model(data):
    param_grid = {  
        'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
        'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
        'seasonality_mode': ['additive', 'multiplicative']
    }

    # Generate all combinations of parameters
    all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
    rmses = []  # Store the RMSEs for each params here

    # Use cross validation to evaluate all parameters
    for idx, params in enumerate(all_params):
        print("===== Model ",idx," of ", len(all_params), " =====")
        m = Prophet(**params).fit(data)  # Fit model with given params
        df_cv = cross_validation(m, horizon='30 days', parallel="processes")
        df_p = performance_metrics(df_cv, rolling_window=1)
        rmses.append(df_p['rmse'].values[0])

    # Find the best parameters
    tuning_results = pd.DataFrame(all_params)
    tuning_results['rmse'] = rmses
    print(tuning_results)


def __evaluate_model(model, dataset):
    len_train = round(dataset.shape[0] * 0.75)
    len_test = len(dataset) - len_train
    train = dataset[:len_train]
    test = dataset[len_train:]

    model.fit(train)
    future = model.make_future_dataframe(periods=len_test)
    forecast = model.predict(future)

    rms = mean_squared_error(test['y'], forecast[len_train:]['yhat'], squared=False)
    return rms

def forecast_growth_simple(dataset, time, delta='D'):
    prep_data = __prepare_data(dataset)

    #model_add = Prophet(yearly_seasonality=True, seasonality_mode='additive')
    model_mul = Prophet(yearly_seasonality=True, seasonality_mode='multiplicative', weekly_seasonality=True)
    model_mul.add_country_holidays("PTE")           #TODO_FUTURE add country possibility

    #rms1 = __evaluate_model(model_add, prep_data)
    rms2 = __evaluate_model(model_mul, prep_data)

    #if rms1 > rms2:
    #    best = model_mul
    #else:
    #    best = model_add
    best = model_mul
    future = best.make_future_dataframe(periods=time)
    forecast = best.predict(future)
    
    return forecast

def forecast_growth_advanced(dataset, time, delta='D'):
    prep_data = __prepare_data(dataset)
    __calculate_best_model(prep_data)