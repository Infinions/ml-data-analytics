from pymongo import MongoClient


class MongoController:

    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.db.models

    def lookup_model(self, id):
        results = self.db.find_one({'nif': id})
        return results

    def save_model(self, id, model, vectorizer, expiration_date, accuracy):
        data = {
            'nif': id,
            'model': model,
            'vectorizer': vectorizer,
            'expiration_date': expiration_date,
            'accuracy': float(accuracy)
        }

        self.db.replace_one(
            {'nif': id},
            data,
            upsert=True
        )

