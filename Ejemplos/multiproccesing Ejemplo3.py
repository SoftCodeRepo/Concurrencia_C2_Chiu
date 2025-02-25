from multiprocessing import Process, Manager
from time import sleep
import random
import os

def factorial(num,cola):
    f = 1
    for i in range(2,num+1):
        print(f"computando para {__name__} en la iteración {i} para el fact {num}")
        sleep(random.randint(1,3))
        f*=i
    cola.put(f)
    return f

if __name__ == "__main__":
    cola = Manager().Queue() # Se crea una cola compartida usando un mecanismo de verificacion de concurrencia, para leer un archivo
    p1=Process(target=factorial,args=(5,cola,),name="p1")
    p2=Process(target=factorial,args=(8,cola,),name="p2")
    
    p1.start()
    p2.start()
    print(f"Proceso id {os.getpid()}") # Imprime el id del proceso principal
    print(f"El factorial de 5 es {cola.get()}")
    print(f"El factorial de 8 es {cola.get()}")