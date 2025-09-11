import sys
import webbrowser
import requests
import json
from dotenv import load_dotenv, dotenv_values, set_key

load_dotenv()

import os
from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
from pathlib import Path

today = datetime.now()
validity = today + timedelta(days=45)

ACCOUNT_ID = os.getenv("ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN_FACEBOOK")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

BASE_URL = "https://graph.facebook.com/v23.0/"
INSIGHTS_PATH = "/insights"
ACCESS_TOKEN_PATH = "/access_token"

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

def marketing_actions(fields):
    # Data atual
    today = datetime.today()
    # Quantidade de meses anteriores
    months_ago = today - relativedelta(months=2)
    # Usa sempre o inicio do ano corrente
    start_of_year = datetime(today.year, 1, 1)
    # Caso queira usar com quantidade de meses anteriores, basta trocar a quantidade de meses em months_ago
    init_date = months_ago.replace(day=1)

    all_data = []
    current_start = start_of_year
    total_bytes_global = 0

    while current_start < today:
        current_end = (current_start + relativedelta(months=1)) - relativedelta(days=1)
        if current_end > today:
            current_end = today

        print(f"Buscando dados de {current_start.strftime('%Y-%m-%d')} até {current_end.strftime('%Y-%m-%d')}")

        time_range = json.dumps({
            "since": current_start.strftime("%Y-%m-%d"),
            "until": current_end.strftime("%Y-%m-%d")
        })

        params = {
            "time_increment": "1",
            "limit": "100",
            "time_range": time_range,
            "level": "ad",
            "fields": ",".join(fields),
            "access_token": ACCESS_TOKEN
        }

        url = f"{BASE_URL}{ACCOUNT_ID}{INSIGHTS_PATH}"
        total_bytes_month = 0

        while url:
            response = requests.get(url, params=params)
            
            print(f"📡 Status: {response.status_code}")

            if response.status_code != 200:
                raise Exception(f"Erro na API: {response.status_code} - {response.text}")
            
            result = response.json()
            
            # Contabiliza tamanho do conteúdo
            tamanho_bytes = len(response.content)
            total_bytes_month += tamanho_bytes
            total_bytes_global += tamanho_bytes

            page_data = result.get("data", [])
            all_data.extend(page_data)

            paging = result.get("paging", {})
            url = paging.get("next")
            params = None   
        
        print(f"Mes {current_start.strftime('%Y-%m')} concluído. Registros acumulados: {len(all_data)}. Bytes recebidos neste mês: {total_bytes_month}")

        current_start = current_start + relativedelta(months=1)
        time.sleep(1)

        print(f"\n📦 Tamanho total acumulado de registros: {len(all_data)} | Total de bytes: {total_bytes_global}")

        #Caminho da pasta /data na raiz do projeto
        
        data_path.mkdir(exist_ok=True)  # Cria a pasta se não existir

        # Nome do arquivo
        if "reach" in fields:
            caminho_arquivo = data_path / "mkt_principal.json"
        else:
            caminho_arquivo = data_path / "mkt_act_and_act_values.json"

        with open(caminho_arquivo, "w", encoding="utf-8") as file:
            file.write(json.dumps(all_data, indent=4, ensure_ascii=False))

    return print("Processo de download concluído.")

def marketing_status(level):
    url = f"{BASE_URL}{ACCOUNT_ID}/{level}"
    
    fields = "id","name","status"
    
    params = {
        "fields": ",".join(fields),
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params)

    print(f"📡 Status: {response.status_code}")

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")
    
    result = response.json()

    data_path.mkdir(exist_ok=True)  # Cria a pasta se não existir
    
    if level == "campaigns":
        caminho_arquivo = data_path / "campaings_status.json"
    if level == "adsets":
        caminho_arquivo = data_path / "adsets_status.json"
    if level == "ads":
        caminho_arquivo = data_path / "ads_status.json"

    with open(caminho_arquivo, "w", encoding="utf-8") as file:
        file.write(json.dumps(result, indent=4, ensure_ascii=False))
    
    return print("Processo de download concluído.")

def generate_auth_url():
    params = {
        "client_id": APP_ID,  # Substitua pelo seu App ID
        "redirect_uri": r"file:\\\C:\Users\Robert Walker\Desktop\Trabalho\PROJETOS\POWER BI\4_projetos_negociados\fgz_treinamentos\flask\app_graph_api\callback.html",  # Exibe o código na página do Facebook
        "response_type": "code",
        "scope": "read_insights,ads_management,public_profile",
    }

    auth_url = "https://www.facebook.com/v23.0/dialog/oauth?" + "&".join(
        [f"{key}={value}" for key, value in params.items()]
    )

    webbrowser.open(auth_url)

def convert_short_lived_token_to_long_lived_token(app_id, app_secret, short_lived_token):
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,  # Substitua pelo seu App ID real
        "client_secret": app_secret,  # Substitua pelo seu App Secret real
        "fb_exchange_token": short_lived_token,  # Substitua pelo token de curta duração
    }

    response = requests.get(
        f"https://graph.facebook.com/v23.0/oauth{ACCESS_TOKEN_PATH}",
        params=params
    )

    if response.status_code == 200:
        print("Token de longa duração:", response.json())
    else:
        print("Erro:", response.json())

    access_token = response.json().get("access_token")

    return access_token

def update_long_lived_access_token(short_lived_token):
    try:
        new_token = convert_short_lived_token_to_long_lived_token(APP_ID, APP_SECRET, short_lived_token)
        if not new_token:
            return {
                "status": "ERRO",
                "message": "Token inválido ou expirado"
            }
        
        env_path = ROOT_PATH / '.env'
        env_vars = dotenv_values(env_path)
        env_vars['ACCESS_TOKEN'] = new_token
        env_vars['ACCESS_TOKEN_VALIDITY'] = datetime.strftime(validity, "%d/%m/%Y")

        for key, value in env_vars.items():
            set_key(env_path, key, value) # type: ignore
            
        return {
            "status": "OK",
            "message": "Token atualizado com sucesso"
        }
        
    except Exception as e:
        return {
            "status": "ERRO",
            "message": f"Erro ao atualizar token: {str(e)}"
        }
    
