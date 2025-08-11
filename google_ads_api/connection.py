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
from google.auth.transport.requests import Request as gRequest
import webbrowser


load_dotenv()

class UnsafeRequestsSession(gRequest):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.verify = False  # Ignora SSL

def get_root_path():
    """Retorna o caminho absoluto para a raiz do projeto"""
    if getattr(sys, 'frozen', False):
        # Se empacotado como executável
        return Path(sys.executable).parent
    else:
        # Em desenvolvimento
        return Path(__file__).resolve().parent.parent

ROOT_PATH = get_root_path()

def create_authorization_code():
    try:
        print("Criando pelo método 1, caso haja")
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": os.getenv("CLIENT_ID"),
                    "client_secret": os.getenv("CLIENT_SECRET"),
                    "redirect_uris": ["http://localhost:8080/"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=["https://www.googleapis.com/auth/adwords"],
        )

        # Abre o navegador para autenticação e captura o token
        credentials = flow.run_local_server(port=8080, request=UnsafeRequestsSession())

        # Mostra o refresh token
        print("\n✅ Refresh Token gerado com sucesso:")
        print(credentials.refresh_token)

google_link = (
    f"https://accounts.google.com/o/oauth2/v2/auth?"
    f"client_id={os.getenv('CLIENT_ID')}&"
    "redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
    "response_type=code&"
    "scope=https://www.googleapis.com/auth/adwords&"
    "access_type=offline&"
    "prompt=consent"
)


#webbrowser.open(google_link)


def exchange_code_for_tokens(auth_code):
    token_url = "https://oauth2.googleapis.com/token"
    
    data = {
        "code": auth_code,
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",  # Deve ser igual ao usado na geração do código
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data, verify=False)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        expires_in = tokens.get("expires_in")

        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print(f"Expires in: {expires_in} seconds")
        return access_token, refresh_token
    else:
        print(f"Erro ao trocar o código: {response.status_code}")
        print(response.text)
        return None, None
    
exchange_code_for_tokens("4/1AVMBsJiRoy4QKAkcnqhVS1PYL6K3jhtKHAHw7hdGfFCMwtwbNwpqDOYiYLA")