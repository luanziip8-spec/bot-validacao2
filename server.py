from flask import Flask, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "db.json"

# ===== BANCO =====
def carregar_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "links": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

# ===== HOME =====
@app.route("/")
def home():
    return "API online 🚀"

# ===== REGISTRAR =====
@app.route("/registrar")
def registrar():
    codigo = request.args.get("codigo")
    user_id = request.args.get("user_id")
    token = request.args.get("token")

    if not codigo or not user_id or not token:
        return "erro"

    db = carregar_db()

    db["links"][codigo] = {
        "user_id": user_id,
        "validado": False,
        "token": token
    }

    # garante usuário
    if user_id not in db["users"]:
        db["users"][user_id] = {"moedas": 0}

    salvar_db(db)
    print("LINK REGISTRADO:", codigo)

    return "ok"

# ===== CONFIRMAR =====
@app.route("/confirmar")
def confirmar():
    codigo = request.args.get("codigo")
    token = request.args.get("token")

    if not codigo or not token:
        return "negado"

    db = carregar_db()

    if codigo not in db["links"]:
        return "erro"

    link = db["links"][codigo]

    # valida token
    if link["token"] != token:
        return "negado"

    # já usado
    if link["validado"]:
        return "ok"

    user_id = link["user_id"]

    # garante usuário
    if user_id not in db["users"]:
        db["users"][user_id] = {"moedas": 0}

    # adiciona saldo
    link["validado"] = True
    db["users"][user_id]["moedas"] += 3

    salvar_db(db)

    print("SALDO ADICIONADO:", user_id)

    return "ok"

# ===== SALDO =====
@app.route("/saldo")
def saldo():
    user_id = request.args.get("user_id")

    db = carregar_db()
    moedas = db["users"].get(user_id, {}).get("moedas", 0)

    return f"💰 Saldo: {moedas} moedas"

# ===== RESET (OPCIONAL PRA TESTE) =====
@app.route("/reset")
def reset():
    db = {"users": {}, "links": {}}
    salvar_db(db)
    return "resetado"

# ===== RUN =====
app.run(host="0.0.0.0", port=8080)