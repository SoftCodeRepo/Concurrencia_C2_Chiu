from multiprocessing import Process
from time import sleep
import random
import os

def factorial(num):
    f = 1
    for i in range(2,num+1):
        sleep(random.randint(1,3))
        f*=i
        print(f"computando para {__name__} en la iteración {i} para el fact {num} con resultado {f}")
    print(f"El factorial de {num} es {f}")
    return f

if __name__ == "__main__":
    p1=Process(target=factorial,args=(5,),name="p1")
    p2=Process(target=factorial,args=(8,),name="p2")
    
    p1.start()
    p2.start()
    print(f"Proceso id {os.getpid()}") # Imprime el id del proceso principal