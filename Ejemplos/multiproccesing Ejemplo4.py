from multiprocessing import Process, Pipe, Queue, Lock
def conexion(linea):
    linea.send(['001', 'hola'])
   # print(linea.recv())
    linea.close()
    
if __name__ == "main":
    #par = entrada de la tuberia, chil = salida de la tuberia | son los extremos del pipe, ambos pueden recibir y enviar, como un chan de go
    #par recibe, chil envia, con duplex=True se limita quien hace qué
    par, chil = Pipe(duplex=False)
    p1 = Process(target=conexion, args=(chil,))
    p1.start()
    print('dato recibido', par.recv())
    #par.send(['002', 'hola de vuelta'])
    p1.join()