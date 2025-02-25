from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
import time

class Punto(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

def pruebas(val1,val2,arr1,arr2):
    val1.value **= 3
    val2.value /= 3
    arr1 = arr1.value.upper()
    for i in arr2:
        i.x = 24.32
        i.y = 34.21
    time.sleep(2)
    
if __name__ == "__main__":
    lock1 = Lock()
    n1 = Value('i', 23)
    n2 = Value(c_double, 23.4)
    a1 = Array('c', b"hola bebe", lock=False)
    a2 = Array(Punto, [(1.87, 2.3), (2.1, 23.4), (31, 4.1)], lock=lock1)
    process1 = Process(target=pruebas, args=(n1, n2, a1, a2))
    process2 = Process(target=pruebas, args=(n1, n2, a1, a2))
    process1.start()
    process2.start()
    
    print(n1.value)
    print(n2.value)
    print(a1.value)
    print([(a.x, a.y) for a in a2])
    
    process2.join()