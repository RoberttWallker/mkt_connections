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
today = datetime.today()

def update_env_key(env_path: Path, key: str, new_value: str):
    lines = []
    key_found = False

    # Lê o arquivo linha a linha
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith(f"{key}="):
                lines.append(f'{key}="{new_value}"\n')
                key_found = True
            else:
                lines.append(line)

    # Se a chave não existia, adiciona no final
    if not key_found:
        lines.append(f"{key}={new_value}\n")

    # Escreve de volta
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


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


def create_authorization_code():
    try:
        print("Tentando criar pelo método 1 (interno):\n")
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
        credentials = flow.run_local_server(port=8080)

        # Mostra o refresh token
        print("\n✅ Access Token gerado com sucesso:")
        print(credentials.token)
        print("\n✅ Refresh Token gerado com sucesso:")
        print(credentials.refresh_token)
    
    except Exception as e:
        print(f"\nOcorreu o seguninte erro: {e}\n")
        print("Iniciando método direto pelo navegador...")
        print("Não esqueça de colar o token de acesso no software de consumo de dados.")

        try:
            print("\nTentando criar pelo método 2 (externo):\n")
            google_link = (
                f"https://accounts.google.com/o/oauth2/v2/auth?"
                f"client_id={os.getenv('CLIENT_ID')}&"
                "redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
                "response_type=code&"
                "scope=https://www.googleapis.com/auth/adwords&"
                "access_type=offline&"
                "prompt=consent"
            )

            if webbrowser.open(google_link):
                print("\n✅ Link aberto no navegador com sucesso!")
            else:
                print("\n⚠ Não foi possível abrir o navegador automaticamente.")
                print(f"Acesse manualmente o link abaixo:\n{google_link}")

            print("\n📌 Passo a passo:")
            print("1. No navegador, faça login na conta Google desejada.")
            print("2. Aceite as permissões solicitadas.")
            print("3. Será exibido um código de autorização na tela.")
            print("4. Copie esse código e cole no seu software de consumo de dados.")


        except Exception as e:
            print(f"Ocorreu o seguninte erro: {e}\n")
            print("Verifique se o fluxo de autenticação está correto!")

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

def update_access_token(client_id, client_secret, refresh_token):
    url = "https://oauth2.googleapis.com/token"

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Erro ao renovar access_token: {response.status_code} - {response.text}")

    data = response.json()
    access_token = data.get("access_token")
    if not access_token:
        raise Exception(f"Não foi possível obter access_token: {data}")

    env_path = ROOT_PATH / '.env'
    # env_vars = dotenv_values(env_path)
    # env_vars['ACCESS_TOKEN_GOOGLE'] = access_token

    update_env_key(env_path, "ACCESS_TOKEN_GOOGLE", access_token)

    return access_token

def get_query_response(mkt_query):
    url = f"https://googleads.googleapis.com/v21/customers/{os.getenv('CUSTOMER_ID')}/googleAds:searchStream"
    headers = {
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN_GOOGLE')}",
        "developer-token": os.getenv('DEVELOPER_TOKEN'),
        "Content-Type": "application/json"
    }
    body = {"query": mkt_query}

    response = requests.post(url, headers=headers, json=body)
    return response

def google_mkt_data():
    months_ago = today - relativedelta(months=2)
    start_of_year = datetime(today.year-1, 1, 1)
    init_date = months_ago.replace(day=1)

    total_bytes_global = 0
    current_start = start_of_year

    # Caminho do arquivo final
    data_path.mkdir(exist_ok=True)
    caminho_arquivo = data_path / "google_ads_data.json"

    with open(caminho_arquivo, "w", encoding="utf-8") as file:
        file.write("[\n")  # início do JSON
        first_row = True  # flag para adicionar vírgula entre rows

        while current_start < today:
            current_end = (current_start + relativedelta(months=1)) - relativedelta(days=1)
            if current_end > today:
                current_end = today

            print(f"📅 Buscando dados de {current_start.strftime('%Y-%m-%d')} até {current_end.strftime('%Y-%m-%d')}")

            mkt_query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                segments.date,
                segments.device,
                segments.ad_network_type,
                segments.hour,

                metrics.impressions,
                metrics.clicks,
                metrics.ctr,
                metrics.average_cpc,
                metrics.cost_micros,
                metrics.conversions
             FROM campaign
             WHERE segments.date BETWEEN '{current_start.strftime("%Y-%m-%d")}' AND '{current_end.strftime("%Y-%m-%d")}'
             ORDER BY
                segments.date
            """

            # url = f"https://googleads.googleapis.com/v21/customers/{os.getenv('CUSTOMER_ID')}/googleAds:searchStream"
            # headers = {
            #     "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN_GOOGLE')}",
            #     "developer-token": os.getenv('DEVELOPER_TOKEN'),
            #     "Content-Type": "application/json"
            # }
            # body = {"query": mkt_query}
            
            response = get_query_response(mkt_query)
            
            print(f"📡 Status: {response.status_code}")
            if response.status_code == 401:
                print(f"Token vencido, iniciando atualização...")     
                token = update_access_token(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'), os.getenv('REFRESH_TOKEN'))
                os.environ['ACCESS_TOKEN_GOOGLE'] = token
                print(f"Token atualizizado com sucesso! ACCESS_TOKEN: {token}")

                response = get_query_response(mkt_query)

            if response.status_code != 200:
                raise Exception(f"Erro na API Google Ads: {response.status_code} - {response.text}")

            results = response.json()
            total_bytes_month = 0

            # escreve cada row direto no arquivo
            for batch in results:
                for row in batch.get("results", []):
                    if not first_row:
                        file.write(",\n")
                    file.write(json.dumps(row, indent=4, ensure_ascii=False))
                    first_row = False
                    total_bytes_month += len(json.dumps(row, ensure_ascii=False).encode('utf-8'))
                    total_bytes_global += len(json.dumps(row, ensure_ascii=False).encode('utf-8'))

            print(f"✅ Mês {current_start.strftime('%Y-%m')} concluído. Bytes recebidos neste mês: {total_bytes_month}")

            current_start = current_start + relativedelta(months=1)
            time.sleep(1)  # evita estourar limites de requisição

        file.write("\n]")  # final do JSON

    print(f"\n📦 Tamanho total de bytes acumulado: {total_bytes_global}")
    print("💾 Arquivo salvo com sucesso:", caminho_arquivo)


google_mkt_data()
#create_authorization_code()
