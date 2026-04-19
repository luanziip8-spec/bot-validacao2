from flask import Flask, request
import json
import os

app = Flask(__name__)
DB_FILE = "db.json"

def carregar_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "links": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

@app.route("/confirmar")
def confirmar():
    codigo = request.args.get("codigo")

    db = carregar_db()

    if codigo not in db["links"]:
        return "erro"

    if db["links"][codigo]["validado"]:
        return "ok"

    user_id = db["links"][codigo]["user_id"]

    db["links"][codigo]["validado"] = True
    db["users"][user_id]["moedas"] += 3

    salvar_db(db)

    return "ok"

app.run(host="0.0.0.0", port=8080)
