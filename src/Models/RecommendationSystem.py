import numpy as np
import pandas as pd
import os
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import psycopg2 as pg
from datetime import datetime, timedelta
import Data.load_data


dbname = os.getenv('DB_MODEL_NAME') if os.getenv('DB_NAME') != None else "infin_models"
dbuser = os.getenv('DB_USER') if os.getenv('DB_USER') != None else "infin"
dbpwd  = os.getenv('DB_PWD') if os.getenv('DB_PWD') != None else "infin"
dbport  = os.getenv('DB_PORT') if os.getenv('DB_PORT') != None else "5432"
dbHost = os.getenv('DB_HOST') if os.getenv('DB_HOST') != None else "localhost"

class RecommendationSystem:

    def __init__(self, nif):
        self.connection = pg.connect(dbname=dbname, user=dbuser, password=dbpwd,
                        host=dbHost, port=dbport)
        self.nif = nif
        self.X = []
        self.Y = []
        self.model
        self.EXPIRATION_TIME = 15   # days

    def check_existing_model(self):
        load_model_query = """SELECT * FROM models
                            where nif=(%s)
                           """

        cur = self.connection.cursor()
        cur.execute(load_model_query, (self.nif,))
        results = curr.fetchall()
        if results is empty or results[0][2] >= datetime.now():
            return False

        return True

    def prepare_data(self):
        dataset = Data.load_data(self.nif)
        dataset['company_seller_name'] = dataset['company_seller_name'].apply(lambda c: c.replace(" ",""))
        dataset['date'] = pd.to_datetime(dataset['date']).astype(int)/ 10**9
        
        tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words='portuguese')
        X1 = tfidfconverter.fit_transform(dataset['company_seller_name']).toarray()
        
        self.X = pd.DataFrame(X1)
        self.X['value'] = dataset['total_value'].values
        self.X['date'] = dataset['date'].values 
        self.Y = dataset['category_id']

    def save_model(self):
        inser_model_query = """INSERT INTO models(nif, model, expiration_date, accuracy)
                                VALUES(%s)"""

        pickled_model = pickle.dumps(self.model)
        expiration_date = datetime.now() + timedelta(days = self.EXPIRATION_TIME)

        cur = self.connection.cursor()
        cur.execute(inser_model_query, (self.nif, pickled_model, expiration_date, self.accuracy,))
        self.connection.commit()
        cur.close()

    def load_model(self):
        load_model_query = """SELECT * FROM models
                            where nif=(%s)
                           """

        cur = self.connection.cursor()
        cur.execute(load_model_query, (self.nif,))

        db_model = curr.fetchall()[0][1]
        self.model = pickle.loads(db_model)
        cur.close()

    def train_model(self):
        params = {
            'n_estimators': [10, 100],
            'criterion': ['gini','entropy']
        }
    
        gs = GridSearchCV(RandomForestClassifier(), params, cv=3, n_jobs=-1, verbose=1)
        gs_results = gs.fit(self.X, self.Y)
        self.model = gs_results.best_estimator_
        self.accuracy = gs_results.best_score_

    def __prepare_new_data(self, data):
        tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words='portuguese')
        x = tfidfconverter.fit_transform(data['company_seller_name']).toarray()

        return x

    def recommend_category(self, data):
        x = self.__prepare_new_data(data)
        category = self.model.predict(x)
        # TODO convert id to Name
        return category