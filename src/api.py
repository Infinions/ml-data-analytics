from flask import Flask, request,send_from_directory
from flask_cors import CORS
import os
import json

import Data.load_data as load_data
import Models.manipulation as data_manipulation

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

    json_data1 = res1.to_json(orient='values')
    json_data2 = res2.to_json(orient='values')

    return {'costs': json_data1, 'earnings': json_data2}
