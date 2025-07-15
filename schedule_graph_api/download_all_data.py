import sys
import os
import logging
from datetime import datetime

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_graph_api import connection

# Configuração do logging
logging.basicConfig(
    filename='log_download_all_data.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível mínimo de mensagens a registrar
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

if __name__ == "__main__":
    logging.info("Iniciando o download dos arquivos...")

    fields_marketing_actions = [
    "ad_id", "ad_name", "adset_id", "adset_name",
    "campaign_id", "campaign_name", "spend",
    "actions", "action_values"
    ]

    fields_principal = [
        "impressions","reach","cpm","ctr","ad_id"
    ]

    try:
        logging.info("Executando Marketing Actions...")
        connection.marketing_actions(fields_marketing_actions)
        logging.info("Marketing Actions Finalizado.")
        
    except Exception as e:
        logging.exception(f"Erro durante execução de marketing_actions() {e}")
        
    try:
        logging.info("Executando Marketing Principal...")
        connection.marketing_actions(fields_principal)                
        logging.info("Marketing Principal Finalizado.")
    except Exception as e:
        logging.exception(f"Erro durante execução de marketing_actions() {e}")