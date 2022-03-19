# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from .import_data import upload
from django.urls import path, re_path
from apps.home.views import index, companydetails, search

urlpatterns = [

    # The home page
    path('', index, name='home'),
    path('company/<int:cik>', companydetails, name='company'),
    path('search/',search,name='search_company'),
    path('import-csv/', upload),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
