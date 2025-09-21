import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph_api import connection

# Configuração do logging
logging.basicConfig(
    filename='log_facebook_download_all_data.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível mínimo de mensagens a registrar
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    encoding='utf-8'
)

if __name__ == "__main__":
    logging.info("Iniciando o download dos arquivos...")

    fields_marketing_actions = [
    "ad_id", "ad_name", "adset_id", "adset_name",
    "campaign_id", "campaign_name", "spend",
    "actions", "action_values"
    ]

    fields_principal = [
        "spend","impressions","reach","cpm","ctr","ad_id"
    ]
    
    try:
        logging.info("\n####### INÍCIO: Marketing Actions #######")
        connection.marketing_actions(fields_marketing_actions)
        logging.info("✅ Marketing Actions finalizado com sucesso.")
        logging.info("####### FIM: Marketing Actions #######\n")

    except Exception as e:
        logging.exception(f"❌ Erro durante execução de marketing_actions() [Actions] - {e}\n")

    # -----------------------------------------------

    try:
        logging.info("\n####### INÍCIO: Marketing Principal #######")
        connection.marketing_actions(fields_principal)
        logging.info("✅ Marketing Principal finalizado com sucesso.")
        logging.info("####### FIM: Marketing Principal #######\n")

    except Exception as e:
        logging.exception(f"❌ Erro durante execução de marketing_actions() [Principal] - {e}\n")

    # -----------------------------------------------

    try:
        levels = ["ads", "adsets", "campaigns"]  # corrigido 'campaings'

        for level in levels:
            logging.info(f"\n####### INÍCIO: Marketing Status - {level.upper()} #######")
            connection.marketing_status(level)
            logging.info(f"✅ Marketing Status para {level.upper()} finalizado com sucesso.")
            logging.info(f"####### FIM: Marketing Status - {level.upper()} #######\n")

    except Exception as e:
        logging.exception(f"❌ Erro durante execução de marketing_status() - {e}\n")
