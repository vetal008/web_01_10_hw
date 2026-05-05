import os

import django
from pymongo import MongoClient


def make_migrate():


    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homework.settings")
    django.setup()

    from quotes.models import Quote, Tag, Author  # noqa

    client = MongoClient("mongodb://localhost")

    db = client.django_hw

    authors = db.authors.find()

    for author in authors:
        print('hello')
        # print(author['author_fullname'])
        Author.objects.get_or_create(
            author_fullname=author['author_fullname'],
            born_date=author['born_date'],
            born_location=author['born_location'],
            description=author['description'],
        )

    quotes = db.quotes.find()

    for quote in quotes:
        tags = []
        for tag in quote['tags']:
            tuple, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(tuple)
        print(tags)

        exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))
        if not exist_quote:
            print(exist_quote)
            author = db.authors.find_one({'_id': quote['author']})
            a = Author.objects.get(author_fullname=author['author_fullname'])
            q = Quote.objects.create(
                quote=quote['quote'],
                author=a,
            )
            for tag in tags:
                q.tags.add(tag)
