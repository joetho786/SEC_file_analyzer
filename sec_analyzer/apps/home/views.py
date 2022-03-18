from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Company
from django.shortcuts import render
import json 
import requests
from .utility import format_cik, get_company_assets, get_company_shares
import pandas as pd 
from django.shortcuts import get_object_or_404

def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def companydetails(request,cik):
    cik = format_cik(str(cik))
    # company = Company.objects.filter()
    headers = {'User-Agent': "your@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json", headers=headers)
    if response.status_code ==200:
        shares_df = get_company_shares(cik)
        shares = list(shares_df['val'])
        filed = list(shares_df['filed'])
        print(shares)
    else:
        shares=[]
        filed = []
    context = {'shares':json.dumps(shares), 
                'filed':filed}
    # print(context['assets'])

    html_template = loader.get_template('home/' + 'company.html')
    return HttpResponse(html_template.render(context, request))


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    load_template = request.path.split('/')[-1]

    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))
    context['segment'] = load_template

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except Exception as e:
    #     print(e)
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))
