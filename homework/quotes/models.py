from django.core.exceptions import ValidationError
from django.db import models

from .utils import get_mongodb


def existing_author(name):
    db = get_mongodb()
    authors = [author['author_fullname'] for author in db.authors.find()]
    if name in authors:
        raise ValidationError('Author "%s" already exists' % name)


# Create your models here.
class Author(models.Model):
    author_fullname = models.CharField(max_length=100, validators=[existing_author])
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author_fullname


class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)  # ✅ замість ArrayField
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quote[:50]
