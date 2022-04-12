import requests
import pandas as pd
import os
from django.conf import settings


def format_cik(cik):
    final_cik = "0"*(10-len(cik))+cik 
    return final_cik

def get_company_current_assets(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "test@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json", headers=headers)
    if response.status_code == 200:
        assets_timeserie = pd.json_normalize(response.json()["units"]["USD"])
        assets_timeserie = assets_timeserie[assets_timeserie['form']=='10-K']
        # assets_timeserie["filed"] = pd.to_datetime(assets_timeserie["filed"])
        assets_timeserie = assets_timeserie.sort_values("end")
        assets_timeserie.to_csv(os.path.join(settings.MEDIA_ROOT, os.path.join('assets', f'{cik}_assets.csv')))
        try:
            current_asset_val =list(assets_timeserie[assets_timeserie['form']=='10-K']['val'])[-1]
        except Exception as e:
            current_asset_val = None
    else:
        current_asset_val =None
    return current_asset_val

def get_company_shares(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "yours@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
    if response.status_code == 200:
        js = response.json()
        try:
            company_shares = pd.json_normalize(js['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'])
            company_shares.to_csv(os.path.join(settings.MEDIA_ROOT, os.path.join('shares', f'{cik}_shares.csv')))
            ten_share = company_shares[company_shares['form']=='10-K']
        except Exception as e:
            ten_share = None
        # print(ten_share)
    else:
        ten_share = None
    return ten_share

def get_10K_links(cik):
    cik_10k = pd.read_csv("https://sagemaker-studio-chq5a4fyzh5.s3.amazonaws.com/b+(1).csv")
    cik_10k.fillna('nan',inplace=True)
    try:
        cik_10k = cik_10k[cik_10k['cik']==int(cik)].iloc[0,1:].to_dict()
    except Exception as e:
        return None
    # print(cik_10k)
    return cik_10k

def get_liabilities(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "mine@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
    if response.status_code == 200:
        js = response.json()
        try:
            company_liabilities = pd.json_normalize(js['facts']['us-gaap']['Liabilities']['units']['USD'])
            annual_liability = company_liabilities[company_liabilities['form']=='10-K']
        except Exception as e:
            annual_liability = None
    else: 
        annual_liability = None   
    return annual_liability


def get_performance(ticker):
    
    get_scores_df = pd.read_csv(os.path.join(settings.MEDIA_ROOT,'ml_scores/all_scores.csv'))
    try:
        performance = get_scores_df[get_scores_df['ticker']==ticker]
        p_columns = performance.columns
        if len(performance)>1:
            performance = performance.iloc[0,:]
        # print(performance)
    except Exception as e:
        performance = None
        p_columns = None
    # print(performance)
    return performance, p_columns
