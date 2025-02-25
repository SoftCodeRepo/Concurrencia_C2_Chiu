from multiprocessing.managers import BaseManager

BaseManager.register('get_mycola')
manager = BaseManager(address=('127.0.0.1', 5000), authkey=b'abcd')
manager.connect()

print(manager.get_mycola().get())