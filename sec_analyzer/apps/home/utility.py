import requests
import pandas as pd

def format_cik(cik):
    final_cik = "0"*(10-len(cik))+cik 
    return final_cik

def get_company_assets(cik):
    cik = format_cik(cik)
    headers = {'User-Agent': "your@gmail.com"}
    response = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json", headers=headers)
    assets_timeserie = pd.json_normalize(response.json()["units"]["USD"])
    assets_timeserie = assets_timeserie[assets_timeserie['form']=='10-K']
    # assets_timeserie["filed"] = pd.to_datetime(assets_timeserie["filed"])
    assets_timeserie = assets_timeserie.sort_values("end")
    return assets_timeserie

def get_company_shares(cik):
    headers = {'User-Agent': "bhavsar.2@iitj.ac.in"}
    response = requests.get("https://data.sec.gov/api/xbrl/companyfacts/CIK0001459417.json", headers=headers)
    js = response.json()
    company_shares = pd.json_normalize(js['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'])
    # assets_timeserie["filed"] = pd.to_datetime(assets_timeserie["filed"])
    # assets_timeserie = assets_timeserie.sort_values("end")
    ten_share = company_shares[company_shares['form']=='10-K']
    # print(ten_share)
    return ten_share['val']
