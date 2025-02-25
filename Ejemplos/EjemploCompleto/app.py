from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)
with Listener(address, authkey=b'12345') as listener:
    with listener.accept() as conn:
        print("conexion aceptada de: ", listener.last_accepted)
        conn.send([2.8, "Hola", None, float])
        conn.send_bytes(b"hola 7b")
        conn.send_bytes(array('i',[1,2,3,4]))