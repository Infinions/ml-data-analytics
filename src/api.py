from flask import Flask, request
from flask_graphql import GraphQLView
import os
import json
from pandas import DataFrame
from Schemas.schema import RootQuery
from graphene import Schema

port = os.getenv('API_PORT') if os.getenv('API_PORT') != None else "5600"

app = Flask(__name__)

schema = Schema(query=RootQuery, auto_camelcase=False)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))


if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')