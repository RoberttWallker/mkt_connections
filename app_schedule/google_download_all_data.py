import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google_ads_api import connection

# Configuração do logging
logging.basicConfig(
    filename='log_google_download_all_data.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível mínimo de mensagens a registrar
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    encoding='utf-8'
)

if __name__ == "__main__":
    logging.info("Iniciando o download dos arquivos...")

    try:
        logging.info("\n####### INÍCIO: Marketing Data #######")
        connection.google_mkt_data_2()
        logging.info("✅ Marketing Data finalizado com sucesso.")
        logging.info("####### FIM: Marketing Data #######\n")

    except Exception as e:
        logging.exception(f"❌ Erro durante execução de google_mkt_data_2() - {e}\n")