import multiprocessing
import time
import random

TOTAL_LUGARES = 8
PRECIO_POR_10S = 5  # Precio por cada 10 segundos

def gestionar_entrada(estacionamiento, tiempos_estancia, stop_event, semaforo_entrada_Salida):
    while not stop_event.is_set():
        time.sleep(random.uniform(2, 4))
        semaforo_entrada_Salida.acquire()
        
        if None in estacionamiento:
            lugar = estacionamiento.index(None)
            auto_id = f"Auto-{random.randint(1000, 9999)}"
            estacionamiento[lugar] = auto_id
            tiempos_estancia[auto_id] = random.randint(30, 60)
            print(f"Entrada: {auto_id} estacionado en el lugar {lugar + 1} por {tiempos_estancia[auto_id]}s.")
        else:
            print("Entrada: Estacionamiento lleno, no se puede entrar.")
        
        semaforo_entrada_Salida.release()

def gestionar_salida(estacionamiento, tiempos_estancia, stop_event, semaforo_entrada_Salida):
    while not stop_event.is_set():
        time.sleep(random.uniform(2, 4))
        semaforo_entrada_Salida.acquire()
        
        lugares_ocupados = [i for i, auto in enumerate(estacionamiento) if isinstance(auto, str)]
        if lugares_ocupados:
            lugar = random.choice(lugares_ocupados)
            auto_id = estacionamiento[lugar]
            print(f"Salida: {auto_id} saliendo del lugar {lugar + 1}.")
            estacionamiento[lugar] = None
            if auto_id in tiempos_estancia:
                del tiempos_estancia[auto_id]
        else:
            print("Salida: No hay autos en el estacionamiento.")
        
        semaforo_entrada_Salida.release()

def cobrar_tiempo(tiempos_estancia, stop_event, pipe_conn):
    total_dinero = 0

    while not stop_event.is_set():
        time.sleep(10)  # Cobro cada 10s
        autos_actuales = list(tiempos_estancia.keys())  # Autos en el estacionamiento
        
        for auto in autos_actuales:
            if tiempos_estancia[auto] > 0:
                total_dinero += PRECIO_POR_10S
                tiempos_estancia[auto] -= 10  # Reducir tiempo restante
                print(f"Cobro: {auto} paga {PRECIO_POR_10S} pesos. Total acumulado: {total_dinero} pesos.")

        pipe_conn.send(total_dinero)  # Enviar el total actualizado

    pipe_conn.send(total_dinero)  # Enviar el total final
    pipe_conn.close()

def supervisor_estacionamiento(estacionamiento, stop_event):
    while not stop_event.is_set():
        time.sleep(5)
        lugares_ocupados = sum(1 for lugar in estacionamiento if isinstance(lugar, str))
        print(f"Supervisor: {lugares_ocupados}/{TOTAL_LUGARES} lugares ocupados.")

def apartar_lugares(estacionamiento, stop_event, semaforo_entrada_Salida):
    while not stop_event.is_set():
        time.sleep(random.uniform(1, 5))
        semaforo_entrada_Salida.acquire()
        
        lugares_disponibles = [i for i, lugar in enumerate(estacionamiento) if lugar is None]
        if lugares_disponibles:
            num_apartados = random.randint(1, min(3, len(lugares_disponibles)))
            lugares_a_apartar = random.sample(lugares_disponibles, num_apartados)
            for lugar in lugares_a_apartar:
                estacionamiento[lugar] = "Apartado"
            print(f"Apartar: Se han reservado {num_apartados} lugares.")
        
        semaforo_entrada_Salida.release()

if __name__ == "__main__":
    multiprocessing.freeze_support()

    manager = multiprocessing.Manager()
    estacionamiento = manager.list([None] * TOTAL_LUGARES)
    tiempos_estancia = manager.dict()
    stop_event = multiprocessing.Event()
    semaforo_entrada_Salida = multiprocessing.Semaphore(2)

    parent_conn, child_conn = multiprocessing.Pipe()

    procesos = [
        multiprocessing.Process(target=gestionar_entrada, args=(estacionamiento, tiempos_estancia, stop_event, semaforo_entrada_Salida)),
        multiprocessing.Process(target=gestionar_salida, args=(estacionamiento, tiempos_estancia, stop_event, semaforo_entrada_Salida)),
        multiprocessing.Process(target=cobrar_tiempo, args=(tiempos_estancia, stop_event, child_conn)),
        multiprocessing.Process(target=supervisor_estacionamiento, args=(estacionamiento, stop_event)),
        multiprocessing.Process(target=apartar_lugares, args=(estacionamiento, stop_event, semaforo_entrada_Salida))
    ]

    # Iniciar procesos
    for p in procesos:
        p.start()

    try:
        tiempo_inicio = time.time()
        while time.time() - tiempo_inicio < 240:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")

    stop_event.set()

    for p in procesos:
        p.join()

    total_final = 0
    while parent_conn.poll():
        total_final = parent_conn.recv()

    print(f"\nTotal de dinero recaudado: {total_final} pesos.")
    print("Finalizado.")
