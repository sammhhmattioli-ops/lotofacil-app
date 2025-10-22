import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, send_from_directory
import json, os, random, threading, time

app = Flask(__name__, static_folder='static', static_url_path='/static')
BASE = os.path.dirname(__file__)
HIST_FILE = os.path.join(BASE, 'historico.json')
CSV_FILE = os.path.join(BASE, 'jogos_3519.csv')
CONFIG_FILE = os.path.join(BASE, 'config.json')

def load_historico():
    if not os.path.exists(HIST_FILE):
        return []
    with open(HIST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_historico(hist):
    with open(HIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

def atualizar_historico():
    url = "https://www.megaloterias.com.br/lotofacil"  # exemplo, parse simplificado
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # aqui você adicionaria parse do HTML para extrair concurso, data e dezenas
        # como exemplo, adicionamos um concurso fictício
        historico = load_historico()
        novo_concurso = {"concurso": 3520, "dezenas": random.sample(range(1,26),15)}
        if not any(c["concurso"]==novo_concurso["concurso"] for c in historico):
            historico.append(novo_concurso)
            save_historico(historico)
    except Exception as e:
        print("Erro ao atualizar historico:", e)

def job_atualizar():
    while True:
        atualizar_historico()
        time.sleep(60*30)  # atualiza a cada 30 minutos

def carregar_config():
    default = {"num_repetidas":9,"num_extras":6,"soma_min":170,"soma_max":220,"min_pares":6,"max_pares":9}
    if not os.path.exists(CONFIG_FILE):
        return default
    with open(CONFIG_FILE,'r',encoding='utf-8') as f:
        return json.load(f)

def gerar_jogos(n):
    historico = load_historico()
    cfg = carregar_config()
    if historico:
        ultimo = historico[-1].get("dezenas",[])
    else:
        ultimo = []
    jogos = []
    for _ in range(n):
        repetidas = random.sample(ultimo, cfg["num_repetidas"]) if len(ultimo)>=cfg["num_repetidas"] else random.sample(range(1,26), cfg["num_repetidas"])
        extras_pool = [d for d in range(1,26) if d not in repetidas]
        extras = random.sample(extras_pool, cfg["num_extras"])
        jogos.append(sorted(repetidas+extras))
    return jogos

@app.route("/api/jogos")
def api_jogos():
    jogos = []
    with open(CSV_FILE,'r',encoding='utf-8') as f:
        lines = f.read().strip().splitlines()
        headers = lines[0].split(',')
        for line in lines[1:]:
            parts = line.split(',')
            entry = {headers[i]: parts[i] for i in range(len(parts))}
            jogos.append(entry)
    return jsonify({"jogos":jogos})

@app.route("/api/gerar/<int:n>")
def api_gerar(n):
    return jsonify({"jogos":gerar_jogos(n)})

@app.route("/")
def index():
    return send_from_directory('static','index.html')

if __name__=="__main__":
    thread = threading.Thread(target=job_atualizar, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000)
