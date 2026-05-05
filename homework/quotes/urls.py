# from django.contrib import admin
from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path("<int:page>", views.main, name='root_paginate'),
    path('load_sql', views.load_sql, name='load_sql'),
    path('add_quote', views.add_quote, name='add_quote'),
    path('add_author', views.add_author, name='add_author'),
    path("author/<str:author_id>/", views.author_detail, name="author_detail")
]
