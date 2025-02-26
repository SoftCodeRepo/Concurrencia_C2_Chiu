from time import sleep
from multiprocessing import Manager,Process, freeze_support
from multiprocessing.managers import BaseManager


clientes = []

def monitor():
    while True:
        print("Clientes conectados: ", len(clientes))
        sleep(2)
    
def registro(datos):
    clientes.append(datos)
    
def registro_desconexion(datos):
    clientes.pop(datos)
    
class myMaganer(BaseManager):
    pass

if __name__ == '__main__':
    freeze_support()
    clientes = Manager().list()
    myMaganer.register('get_registro', callable=registro)
    myMaganer.register('get_desconexion', callable=registro_desconexion)
    
    manag = myMaganer(address=('localhost', 5000), authkey = b'123')
    manag.start()
    
    p1 = Process(target=monitor, daemon=True)
    p1.start()
    
    try:
        while True:
            print("Servidor en servicio")
            sleep(2)
    except KeyboardInterrupt:
        print("Servidor detenido")
    finally:
        manag.shutdown()
        