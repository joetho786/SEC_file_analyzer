# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Data(models.Model):
    cik = models.CharField(max_length=10)
    ticker = models.CharField(max_length=5)
    company = models.CharField(max_length=50)

