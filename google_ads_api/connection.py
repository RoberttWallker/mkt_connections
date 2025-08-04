import sys
import requests
import json
import os
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
from dotenv import load_dotenv, dotenv_values, set_key
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

config = {
    "developer_token": os.getenv("DEVELOPER_TOKEN"),
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET"),
    "refresh_token": os.getenv("REFRESH_TOKEN"),
    "login_customer_id": os.getenv("LOGIN_CUSTOMER_ID"),
    "use_proto_plus": True
}

def get_root_path():
    """Retorna o caminho absoluto para a raiz do projeto"""
    if getattr(sys, 'frozen', False):
        # Se empacotado como executável
        return Path(sys.executable).parent
    else:
        # Em desenvolvimento
        return Path(__file__).resolve().parent.parent

ROOT_PATH = get_root_path()
data_path = ROOT_PATH / "data"

client = GoogleAdsClient.load_from_dict(config)

# Substitua pelo ID da sua conta (sem hífen)
customer_id = os.getenv("CUSTOMER_ID")

def create_refresh_token():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
    )

    credentials = flow.run_local_server(port=8080)
    print("Refresh Token:", credentials.refresh_token)

create_refresh_token()



# Query com o recurso click_view (nível de clique, inclui gclid)
query = """
SELECT
  campaign.id,
  campaign.name,
  ad_group.id,
  ad_group.name,
  ad_group_criterion.keyword.text,
  click_view.gclid,
  click_view.gclid_date_time,
  metrics.cost_micros
FROM click_view
WHERE segments.date BETWEEN '2025-08-01' AND '2025-08-02'
"""

try:
    ga_service = client.get_service("GoogleAdsService")
    response = ga_service.search_stream(customer_id=customer_id, query=query)

    for batch in response:
        for row in batch.results:
            print({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "ad_group_id": row.ad_group.id,
                "ad_group_name": row.ad_group.name,
                "keyword": row.ad_group_criterion.keyword.text if row.ad_group_criterion.keyword else None,
                "gclid": row.click_view.gclid,
                "click_time": row.click_view.gclid_date_time,
                "cost": int(row.metrics.cost_micros) / 1_000_000
            })

except GoogleAdsException as ex:
    for error in ex.failure.errors:
        print(f"Erro: {error.message}")
