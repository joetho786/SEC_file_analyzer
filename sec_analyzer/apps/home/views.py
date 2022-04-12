from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from urllib3 import HTTPResponse
from .models import Company
from django.shortcuts import redirect, render
import json 
import requests
from .utility import format_cik, get_company_current_assets, get_company_shares, get_10K_links, get_liabilities, get_performance
import pandas as pd 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def index(request):
    search_list = Company.objects.all()
    context = {'segment': 'index',
                'search_list': search_list}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def search(request):
    try:
        company = Company.objects.get(company=request.POST.get('company'))
    except Company.DoesNotExist:
        company =None
    if company is not None:
        return HttpResponseRedirect(reverse('company',args=[company.cik]))
    else:
        return HttpResponseRedirect(reverse('company',args=[0]))

def companydetails(request,cik):
    try: 
        company = Company.objects.get(cik = cik)
    except Company.DoesNotExist:
        company = None
    show_performance = 1
    if company:
        performance_df,p_columns = get_performance(company.ticker)
        # print(performance_df)
        if performance_df is not None or p_columns is not None:
            performance_parameters = list(p_columns)[2:-1]
            performance_values = list(performance_df)[2:-1]
            
        else:
            show_performance = 0
            performance_parameters = None
            performance_values = None
            print(performance_values)
            print(performance_parameters)
    else: 
        show_performance = 0
        performance_parameters = None
        performance_values = None

    cik = format_cik(str(cik))
    search_list = Company.objects.all()
    headers = {'User-Agent': "your@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json", headers=headers)
    # show_liability = 1
    # show_shares = 1
    current_asset = get_company_current_assets(cik)
  
    shares_df = get_company_shares(cik)
    if shares_df is None:
        show_shares = 0
        shares=None
        filed = None
        current_share = None 
        percent_change = None
    else:
        show_shares = 1
        shares = list(shares_df['val'])
        filed = list(shares_df['filed'])
       
        if len(shares)>1:
            current_share =shares[-1]
            percent_change = (shares[-1] - shares[-2])/shares[-2]
        else:
            current_share = None
            percent_change = None
    
    section_10K = get_10K_links(cik)

    liability_df = get_liabilities(cik)
    if liability_df is not None:
        show_liability = 1
        liabilities = list(liability_df['val'])
        lfiled = list(liability_df['filed'])
    else:
        liabilities = []
        show_liability = 0
        lfiled = []

    asset_download_name = f'{cik}_assets.csv'
    shares_download_name = f'{cik}_shares.csv'
    context = {'shares':json.dumps(shares), 
                'filed':filed,
                'search_list':search_list,
                'company':company,
                'current_share':current_share,
                'percent_change':percent_change,
                'sections_10':section_10K,
                'liabilities':json.dumps(liabilities),
                'lfiled': lfiled,
                'show_lia':show_liability,
                'current_asset': current_asset,
                'asset_download': asset_download_name,
                'shares_download': shares_download_name,
                'show_shares':show_shares,
                'show_performance':show_performance, 
                'performance_values':json.dumps(performance_values), 
                'performance_parameters': performance_parameters,
                }
    # print(context['liabil'])

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
