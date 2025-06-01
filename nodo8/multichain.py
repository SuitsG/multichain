from savoir import Savoir

# Configuración de la conexión
rpcuser = 'multichainrpc'  # Usuario RPC por defecto
rpcpasswd = 'contraseña_rpc'  # Reemplaza con la contraseña RPC real
rpchost = 'localhost'
rpcport = '8332'  # Puerto RPC del nodo
chainname = 'mi_cadena'

# Crear una instancia de conexión
api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)

# Consultar el saldo de una dirección
def consultar_saldo(direccion):
    saldo = api.getaddressbalances(direccion)
    print(f"Saldo de la dirección {direccion}: {saldo}")
    return saldo

# Verificar si una dirección tiene saldo suficiente
def verificar_saldo(direccion, cantidad):
    saldo = api.getaddressbalances(direccion)
    for item in saldo:
        if item['qty'] >= cantidad:
            return True
    return False

# Realizar una transacción entre direcciones
def realizar_transaccion(origen, destino, cantidad):
    if verificar_saldo(origen, cantidad):
        txid = api.sendfrom(origen, destino, cantidad)
        print(f"Transacción realizada. ID: {txid}")
        return txid
    else:
        print("Saldo insuficiente.")
        return None

# Mostrar un resumen de las transacciones realizadas
def resumen_transacciones():
    transacciones = api.listtransactions()
    for tx in transacciones:
        print(f"ID: {tx['txid']}, Desde: {tx.get('addresses', [''])[0]}, Cantidad: {tx['amount']}")
