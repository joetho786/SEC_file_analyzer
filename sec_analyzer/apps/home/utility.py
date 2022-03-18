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

