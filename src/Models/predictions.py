from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
import itertools
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from Data.load_data import clean_missing_data
import matplotlib.pyplot as plt

def __prepare_data(data):
    """Prepare data for training.
    Args:
        data: Dataframe, dataset.
    """
    pr_data = data[['dates','total_value']]
    #pr_data['total_value'] = np.log(pr_data['total_value'])
    pr_data.columns = ['ds','y']
    pr_data['ds'] = pd.to_datetime(pr_data['ds'])

    pr_data = pr_data.set_index('ds')

    pr_data = clean_missing_data(pr_data, 'ds','y')

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
    """Forecast the data by _time_ window, with simple method.
    Args:
        model: Prophet, model to evaluate.
        dataset: Dataframe, data to be trained.
    """

    len_train = round(dataset.shape[0] * 0.75)
    len_test = len(dataset) - len_train
    train = dataset[:len_train]
    test = dataset[len_train:]

    model.fit(train)

    future = model.make_future_dataframe(periods=len_test)
    forecast = model.predict(future)
    rms = mean_squared_error(test['y'], forecast[len_train:]['yhat'], squared=False)
    print("======RMS======", rms)
    return rms

def __forecast_growth_simple(prep_data, time):
    """Forecast the data by _time_ window, with simple method.
    Args:
        prep_data: Dataframe, dataset already prepared.
        time: Integer, number of day of forecast.
    """

    country = "PTE"     #TODO_FUTURE add country possibility

    #model_add = Prophet(yearly_seasonality=True, seasonality_mode='additive', weekly_seasonality=True)
    #model_add.add_country_holidays(country)           
    #model_mul = Prophet(yearly_seasonality=True, seasonality_mode='multiplicative', weekly_seasonality=True)
    #model_mul.add_country_holidays(country) 

    #rms1 = __evaluate_model(model_add, prep_data)
    #rms2 = __evaluate_model(model_mul, prep_data)
    #
    #if rms1 > rms2:
    #    best = Prophet(yearly_seasonality=True, seasonality_mode='multiplicative', weekly_seasonality=True)
    #else:
    
    best = Prophet(yearly_seasonality=True, seasonality_mode='additive', weekly_seasonality=False, daily_seasonality=False)
    best.add_country_holidays(country)
    best.fit(prep_data)


    future = best.make_future_dataframe(periods=time)
    forecast = best.predict(future)

    return best, forecast

#TODO CREATE ADVANCED DISCOVERY METHOD
def __forecast_growth_advanced(prep_data, time):
    """Forecast the data by _time_ window, with advanced method.
    Args:
        prep_data: Dataframe, dataset already prepared.
        time: Integer, number of day of forecast.
    """

    __calculate_best_model(prep_data)
    return None, None

def forecast_growth(dataset, time, delta='D', method='simple'):
    """Forecast the data by _time_ window, with simple method.
    Args:
        prep_data: Dataframe, dataset to create model.
        time: Integer, number of day of forecast.
        delta: String, timedelta for showing the data.
        method: String, method of training the model (Simple/Advanced)
    """
    prep_data = __prepare_data(dataset)

    if method == 'advanced':
        _, forecast = __forecast_growth_advanced(prep_data, time)
    else:
        _, forecast = __forecast_growth_simple(prep_data, time)
    

    y_values = forecast[['ds','yhat_lower','yhat','yhat_upper']]
    y_values = y_values.tail(time)

    #If it not daily data
    if delta != 'D':
        y_values = pd.DataFrame(y_values.groupby([pd.Grouper(key='ds', freq=delta)])['yhat_lower','yhat','yhat_upper'].sum()).reset_index()

    y_values = y_values[['ds','yhat']]
    y_values.loc[y_values['yhat'] < 0,'yhat'] = 0
    #y_values['yhat'] = np.exp(y_values['yhat'])
    y_values.columns = ['dates','total_value']
    return y_values