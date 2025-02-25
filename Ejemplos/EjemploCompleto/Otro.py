from multiprocessing.connection import Client
from array import array
from time import sleep

address = ('localhost', 6000)

with Client(address, authkey=b'12345') as cli:
    print(cli.recv())
    sleep(2)
    print(cli.recv_bytes())
    sleep(2)
    arr = array('i', [0,0,0,0,0,0])
    print(cli.recv_bytes_into(arr))
    print(arr)