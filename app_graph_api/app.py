import json
import threading
import time
from flask import Flask, jsonify, send_file
import pandas as pd
import tempfile
import os
import connection
from pathlib import Path

app = Flask(__name__)

ROOT_PATH = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT_PATH / "data"
JSON_FILE = ROOT_PATH / "data" / "mkt_act_and_act_values_teste.json"
CONTADOR_FILE = DATA_PATH / "contador.json"
CACHE_DURATION = 300  # 5 minutos
requisicao = 0

# Variável global para controle de execução
is_processing = False
processing_lock = threading.Lock()

def ler_contador():
    if not CONTADOR_FILE.exists():
        with open(CONTADOR_FILE, "w", encoding="utf-8") as file:
            file.write('{"requisicao": 0}')
        return 0

    try:
        with open(CONTADOR_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("requisicao", 0)
    except Exception as e:
        print(f"Erro ao ler contador: {e}")
        return 0

def incrementar_contador():
    contador = ler_contador() + 1
    with open(CONTADOR_FILE, "w", encoding="utf-8") as f:
        json.dump({"requisicao": contador}, f, indent=4)
    return contador

@app.route("/act-and-act-values")
def retornar_para_power_bi_teste_3():
    global is_processing
    
    with processing_lock:
        if is_processing:
            print("⚠️ Requisição ignorada (processamento em andamento)")
            return "", 204
        
        is_processing = True
    
    try:
        print("🔄 Iniciando processamento...")
        connection.marketing_actions()
            
        # Lê e retorna os dados
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            dados_retorno = json.load(f)
            
        JSON_FILE.unlink()
        
        return jsonify(dados_retorno), 200
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"status": "erro", "msg": str(e)}), 500
        
    finally:
        with processing_lock:
            is_processing = False

@app.route("/act-and-act-values-test") # type: ignore
def retornar_para_power_bi_teste_4():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return jsonify(json.load(file)),200
    except FileNotFoundError:
        return jsonify({"status": "erro", "msg": "Dados não disponíveis"}), 404
if __name__ == "__main__":
    app.run(port=5000)