import multiprocessing
from enum import Enum, auto

class LecturasEspeciales(Enum):
    FINAL = auto()

lectoresEsperando = multiprocessing.Value('i', 0)
lock = multiprocessing.Lock()

class ProcesoReceptor(multiprocessing.Process):
    def __init__(self, queue: multiprocessing.Queue, lectoresEsperando, lock, barrier):
        super().__init__()
        self.queue = queue
        self.lock = lock
        self.lectoresEsperando = lectoresEsperando
        self.barrier = barrier
        
    def run(self):
        print(f"proceso: {self.pid} iniciado, esperando lecturas.")
        with self.lock:
            self.lectoresEsperando.value += 1
        self.barrier.wait()
        while True:
            lectura = self.queue.get()
            if lectura == LecturasEspeciales.FINAL:
                break
            print(f"proceso: {self.pid} ha obtenido la siguiente línea:\n{lectura}")
        with self.lock:
            self.lectoresEsperando.value -= 1
        print(f"proceso: {self.pid} ha terminado sus tareas.")

class ProcesoLector(multiprocessing.Process):
    def __init__(self, queue: multiprocessing.Queue, file: str, lectoresEsperando, lock, barrier):
        super().__init__()
        self.queue = queue
        self.file = file
        self.lock = lock
        self.lectoresEsperando = lectoresEsperando
        self.barrier = barrier
    
    def run(self):
        print(f"proceso: {self.pid} iniciado, leyendo el archivo de texto")
        self.barrier.wait()
        with open(self.file, "r") as file:
            for line in file:
                self.queue.put(line)
        
        with self.lock:
            lectores = self.lectoresEsperando.value
            for _ in range(lectores):
                self.queue.put(LecturasEspeciales.FINAL)
            self.lectoresEsperando.value = 0
        print(f"proceso lector: {self.pid} ha terminado sus tareas.")

if __name__ == "__main__":
    q = multiprocessing.Queue()
    barrier = multiprocessing.Barrier(2 + 1)  # 2 receptores + 1 lector
    pl = ProcesoLector(q, "texto.txt", lectoresEsperando, lock, barrier)
    prs = [ProcesoReceptor(q, lectoresEsperando, lock, barrier) for _ in range(2)]

    pl.start()
    for pr in prs:
        pr.start()
        
    pl.join()
    for pr in prs:
        pr.join()
