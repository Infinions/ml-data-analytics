import numpy as np
import pandas as pd
import os
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from datetime import datetime, timedelta

class RecommendationSystem:

    def __init__(self, nif, db_controller):
        self.db_controller = db_controller
        self.nif = nif
        self.X = []
        self.Y = []
        self.model = 0
        self.vectorizer = 0
        self.EXPIRATION_TIME = 15   # days
        self.accuracy = 0

    def check_existing_model(self):
        result = self.db_controller.lookup_model(self.nif)

        if result is None or result['expiration_date'] <= datetime.now():
            return False

        return True

    def prepare_data(self, dataset):
        dataset['company_seller_name'] = dataset['company_seller_name'].apply(lambda c: c.replace(" ",""))
        dataset['date'] = pd.to_datetime(dataset['date']).astype(int)/ 10**9
        
        self.vectorizer = TfidfVectorizer(max_features=1500, min_df=1, max_df=1, stop_words='english')
        X1 = self.vectorizer.fit_transform(dataset['company_seller_name']).toarray()
        
        self.X = pd.DataFrame(X1)
        self.X['value'] = dataset['total_value'].values
        self.X['date'] = dataset['date'].values 
        self.Y = dataset['category_id']

    def save_model(self):
        pickled_model = pickle.dumps(self.model)
        pickled_vecto = pickle.dumps(self.vectorizer)
        expiration_date = datetime.now() + timedelta(days = self.EXPIRATION_TIME)

        self.db_controller.save_model(self.nif, pickled_model, pickled_vecto, expiration_date, self.accuracy)

    def load_model(self):
        results = self.db_controller.lookup_model(self.nif)
        self.model = pickle.loads(results['model'])
        self.vectorizer = pickle.loads(results['vectorizer'])
        self.accuracy = results['expiration_date']

    def train_model(self):
        params = {
            'n_estimators': [10, 100],
            'criterion': ['gini','entropy']
        }
        try:
            gs = GridSearchCV(RandomForestClassifier(), params, cv=3, n_jobs=-1, verbose=0)
            gs_results = gs.fit(self.X, self.Y)
            self.model = gs_results.best_estimator_
            self.accuracy = gs_results.best_score_
        except ValueError:
            self.model = RandomForestClassifier(criterion='entropy', n_estimators=100, n_jobs=-1, verbose=0) # Default due to lack of enough data to explore model options
            gs_results = self.model.fit(self.X, self.Y)
            self.accuracy = -1
        except:
            print("Something else went wrong")
            exit()


    def __prepare_new_data(self, data):
        data['company_seller_name'] = data['company_seller_name'].apply(lambda c: c.replace(" ",""))
        data['date'] = pd.to_datetime(data['date']).astype(int)/ 10**9
        x = pd.DataFrame(self.vectorizer.transform(data['company_seller_name']).toarray())

        x['value'] = data['total_value'].values
        x['date'] = data['date'].values

        return x

    def recommend_category(self, data):
        x = self.__prepare_new_data(data)

        category = self.model.predict(x)
        return category