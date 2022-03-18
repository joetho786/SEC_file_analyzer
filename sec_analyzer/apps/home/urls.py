# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home.views import index,companydetails

urlpatterns = [

    # The home page
    path('', index, name='home'),
    path('company/<int:cik>',companydetails,name='company')
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
