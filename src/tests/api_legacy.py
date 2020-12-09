from flask import Flask, request
from flask_cors import CORS
import os
import json
from pandas import DataFrame

import Data.load_data as load_data
import Models.statistics as data_manipulation
import Models.predictions as predictor

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/sum_invoices', methods = ['GET'])
def sum_invoices_per_delta():
    timedelta = request.args.get('delta')
    nif = request.args.get('nif')

    data_costs = load_data.load_invoices_from_nif_costs(nif)
    data_earns = load_data.load_invoices_from_nif_earnings(nif)
    res1 = data_manipulation.invoices_sum_per_timedelta(data_costs, timedelta)
    res2 = data_manipulation.invoices_sum_per_timedelta(data_earns, timedelta)

    json_data1 = res1.to_json(orient='records')
    json_data2 = res2.to_json(orient='records')

    return {'costs': json_data1, 'earnings': json_data2}


@app.route('/n_invoices_category', methods = ['GET'])
def n_invoices_per_delta_per_category():
    timedelta = request.args.get('delta')
    nif = request.args.get('nif')
    is_count = request.args.get('is_count')

    data_costs = load_data.load_invoices_from_nif_costs(nif)
    data_earns = load_data.load_invoices_from_nif_earnings(nif)

    if data_costs.empty:
        res1 = DataFrame()
    else:
        res1 = data_manipulation.n_invoices_per_category_per_delta(data_costs, timedelta, is_count)
    
    if data_earns.empty:
        res2 = DataFrame()
    else:
        res2 = data_manipulation.n_invoices_per_category_per_delta(data_earns, timedelta, is_count)

    json_data1 = res1.to_json(orient='records')
    json_data2 = res2.to_json(orient='records')

    return {'costs': json_data1, 'earnings': json_data2}


@app.route('/n_invoices_client', methods = ['GET'])
def n_invoices_per_delta_per_client():
    timedelta = request.args.get('delta')
    nif = request.args.get('nif')
    is_count = request.args.get('is_count')

    data_costs = load_data.load_invoices_from_nif_costs(nif)
    data_earns = load_data.load_invoices_from_nif_earnings(nif)

    if data_costs.empty:
        res1 = DataFrame()
    else:
        res1 = data_manipulation.n_invoices_per_client_per_delta(data_costs, timedelta, is_count)
    
    if data_earns.empty:
        res2 = DataFrame()
    else:
        res2 = data_manipulation.n_invoices_per_client_per_delta(data_earns, timedelta, is_count)

    json_data1 = res1.to_json(orient='records')
    json_data2 = res2.to_json(orient='records')

    return {'costs': json_data1, 'earnings': json_data2}


@app.route('/predict_invoices_simple', methods = ['GET'])
def predict_invoices_simple():
    timedelta = request.args.get('delta')
    nif = request.args.get('nif')
    time = request.args.get('window')

    data_costs = load_data.load_invoices_from_nif_costs(nif)
    data_earns = load_data.load_invoices_from_nif_earnings(nif)

    if data_costs.empty:
        res1 = DataFrame()
    else:
        res1 = predictor.forecast_growth_simple(data_costs, time, timedelta)
    
    if data_earns.empty:
        res2 = DataFrame()
    else:
        res2 = predictor.forecast_growth_simple(data_earns, time, timedelta)

    json_data1 = res1.to_json(orient='records')
    json_data2 = res2.to_json(orient='records')

app.run(debug=True, port=5000)