import multiprocessing

if __name__ == "__main__":
    context = multiprocessing.get_context("spawn")
    manager = context.Manager()
    global_ = manager.Namespace()
    global_.val1 = 20
    global_.val2 = "Hola"
    global_._fantasma = "no me ven"
    print(global_)