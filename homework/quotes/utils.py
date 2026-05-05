from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost")

    db = client.django_hw
    return db

