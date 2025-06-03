from flask import Flask, request, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Configuración MultiChain
rpcuser = 'multichainrpc'
rpcpasswd = '5MxyjyLtwfiz4gAiBecn2LG4sSkTQwbWH54RhqhQekgw'
rpchost = '172.20.0.2'
rpcport = '7725'
chainname = 'chain1'
rpc_url = f'http://{rpchost}:{rpcport}'

def multichain_rpc(method, params=None):
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params or [],
        "id": 1
    }
    response = requests.post(
        rpc_url,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(rpcuser, rpcpasswd)
    )
    response.raise_for_status()
    result = response.json()
    if 'error' in result and result['error']:
        raise Exception(result['error'])
    return result['result']

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/saldo', methods=['POST'])
def saldo():
    data = request.get_json()
    direccion = data.get('direccion')
    if not direccion:
        return jsonify({"error": "Falta la dirección"}), 400
    try:
        balances = multichain_rpc('getaddressbalances', [direccion])
        return jsonify({"direccion": direccion, "balances": balances})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/transaccion', methods=['POST'])
def transaccion():
    data = request.get_json()
    origen = data.get('origen')
    destino = data.get('destino')
    cantidad = data.get('cantidad')
    if not all([origen, destino, cantidad]):
        return jsonify({"error": "Faltan datos"}), 400
    try:
        saldo = multichain_rpc('getaddressbalances', [origen])
        suficiente = any(item['qty'] >= cantidad for item in saldo)
        if not suficiente:
            return jsonify({"error": "Saldo insuficiente"}), 400
        txid = multichain_rpc('sendfrom', [origen, destino, cantidad])
        return jsonify({"txid": txid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resumen', methods=['GET'])
def resumen():
    try:
        # Use '*' to get all transactions, limit to 100 for safety
        transacciones = multichain_rpc('listtransactions', ['*', 100])
        resumen = [
            {
                "txid": tx.get('txid', ''),
                "addresses": tx.get('addresses', []),
                "amount": tx.get('amount', 0)
            }
            for tx in transacciones
        ]
        return jsonify(resumen)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8333, debug=True)