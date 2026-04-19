from flask import Flask, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "db.json"

def carregar_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "links": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

@app.route("/")
def home():
    return "API online"

# ===== REGISTRAR =====
@app.route("/registrar")
def registrar():
    codigo = request.args.get("codigo")
    user_id = request.args.get("user_id")
    token = request.args.get("token")

    db = carregar_db()

    db["links"][codigo] = {
        "user_id": user_id,
        "validado": False,
        "token": token
    }

    if user_id not in db["users"]:
        db["users"][user_id] = {"moedas": 0}

    salvar_db(db)
    return "ok"

# ===== CONFIRMAR =====
@app.route("/confirmar")
def confirmar():
    codigo = request.args.get("codigo")
    token = request.args.get("token")

    db = carregar_db()

    if codigo not in db["links"]:
        return "erro"

    link = db["links"][codigo]

    if link["token"] != token:
        return "negado"

    if link["validado"]:
        return "ok"

    user_id = link["user_id"]

    link["validado"] = True
    db["users"][user_id]["moedas"] += 3

    salvar_db(db)

    return "ok"

# ===== SALDO =====
@app.route("/saldo")
def saldo():
    user_id = request.args.get("user_id")

    db = carregar_db()
    moedas = db["users"].get(user_id, {}).get("moedas", 0)

    return f"💰 Saldo: {moedas} moedas"

app.run(host="0.0.0.0", port=8080)