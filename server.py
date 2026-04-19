from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

@app.route('/check-key')
def check_key():
    codigo = request.args.get("key")

    db = carregar_db()

    if codigo not in db['links_db']:
        return jsonify({"status": "invalid"})

    if db['links_db'][codigo]['validado']:
        return jsonify({"status": "used"})

    return jsonify({"status": "ok"})


# 👇 FORA da rota
def run_api():
    app.run(host="0.0.0.0", port=5000)


# 👇 inicia a API em paralelo com o bot
threading.Thread(target=run_api).start()