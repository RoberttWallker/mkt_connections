import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import win32api

load_dotenv()

today = datetime.now()
validity = os.getenv("ACCESS_TOKEN_VALIDITY")

# Configuração do logging
logging.basicConfig(
    filename='log_check_token_validity.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível mínimo de mensagens a registrar
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    encoding='utf-8'
)

def show_warning_notification():
    """Mostra notificação popup no Windows"""
    message = "⚠️ ATENÇÃO: O token do Facebook expirou!\n\nRenove o token para continuar usando a integração."
    win32api.MessageBox(0, message, "Token Expirado", 0x00001030)  # Ícone de aviso

def check_token_validity():    
    validity_date = datetime.strptime(validity, "%d/%m/%Y") # type: ignore
    if validity_date <= today:
        print(validity)
        print("Vencido")
        logging.info(f"Access Token Vencido! Validade: {validity}")
        show_warning_notification()
    else:
        print(validity)
        print("Na validade")
        logging.info(f"Access Token Dentro da Validade! Validade: {validity}")

if __name__ == "__main__":
    logging.info("Iniciando o download dos arquivos...")

    check_token_validity()