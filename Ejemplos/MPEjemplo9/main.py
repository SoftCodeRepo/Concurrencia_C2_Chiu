from time import sleep

clientes = []

def monitor():
    print(f'Clientes conectados: {len(clientes)}')
    sleep(2)
    
def registro(datos[]):
    clientes.append(datos)
    
def registro_desconexion(datos):
    clientes.pop(datos)