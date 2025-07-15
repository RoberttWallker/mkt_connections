import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
from pathlib import Path

ACCOUNT_ID = os.getenv("ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_URL = "https://graph.facebook.com/v23.0/"
PATH = "/insights"

ROOT_PATH = Path(__file__).resolve().parent.parent

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

        url = f"{BASE_URL}{ACCOUNT_ID}{PATH}"
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
        pasta_data = ROOT_PATH / "data"
        pasta_data.mkdir(exist_ok=True)  # Cria a pasta se não existir

        # Nome do arquivo
        if "reach" in fields:
            caminho_arquivo = pasta_data / "mkt_principal.json"
        else:
            caminho_arquivo = pasta_data / "mkt_act_and_act_values.json"

        with open(caminho_arquivo, "w", encoding="utf-8") as file:
            file.write(json.dumps(all_data, indent=4, ensure_ascii=False))

    return print("Processo de download concluído.")


