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

def get_root_path():
    """Retorna o caminho absoluto para a raiz do projeto"""
    if getattr(sys, 'frozen', False):
        # Se empacotado como executável
        return Path(sys.executable).parent
    else:
        # Em desenvolvimento
        return Path(__file__).resolve().parent.parent

ROOT_PATH = get_root_path()

def create_refresh_token():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
    )

    # Abre o navegador para autenticação e captura o token
    credentials = flow.run_local_server(port=8080)

    # Mostra o refresh token
    print("\n✅ Refresh Token gerado com sucesso:")
    print(credentials.refresh_token)

create_refresh_token()
