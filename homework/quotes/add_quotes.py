import json

from bson import ObjectId
from pymongo import MongoClient


def add_quotes():
    client = MongoClient("mongodb://localhost")
    db = client.django_hw
    with open('quotes.json', 'r', encoding='utf-8') as fd:
        quotes = json.load(fd)
    for quote in quotes:
        print('hello')
        author = db.authors.find_one({'author_fullname': quote['author']})
        if author:
            db.quotes.insert_one({
                'quote': quote['quote'],
                'tags': quote['tags'],
                'author': ObjectId(author['_id'])
            })
