import requests
import pandas as pd
import os

def format_cik(cik):
    final_cik = "0"*(10-len(cik))+cik 
    return final_cik

def get_company_assets(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "your@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json", headers=headers)
    if response.status_code == 200:
        assets_timeserie = pd.json_normalize(response.json()["units"]["USD"])
        assets_timeserie = assets_timeserie[assets_timeserie['form']=='10-K']
        # assets_timeserie["filed"] = pd.to_datetime(assets_timeserie["filed"])
        assets_timeserie = assets_timeserie.sort_values("end")
    return assets_timeserie

def get_company_shares(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "test@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
    if response.status_code == 200:
        js = response.json()
        company_shares = pd.json_normalize(js['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'])
        ten_share = company_shares[company_shares['form']=='10-K']
        # print(ten_share)
    return ten_share

def get_10K_links(cik):
    cik_10k = pd.read_csv("https://sagemaker-studio-chq5a4fyzh5.s3.amazonaws.com/b+(1).csv")
    cik_10k.fillna('nan',inplace=True)
    cik_10k = cik_10k[cik_10k['cik']==int(cik)].iloc[0,1:].to_dict()
    # print(cik_10k)
    return cik_10k

def get_liabilities(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "test@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
    if response.status_code == 200:
        js = response.json()
        try:
            company_liabilities = pd.json_normalize(js['facts']['us-gaap']['Liabilities']['units']['USD'])
            annual_liability = company_liabilities[company_liabilities['form']=='10-K']
        except Exception as e:
            annual_liability = None
        
    return annual_liability
