from .proceso import Proceso

class GestorColas:
    """
    Gestiona las diferentes colas de procesos del sistema (Nuevos, Listos, Suspendidos, etc.).
    """
    def __init__(self):
        self.nuevos = []
        self.listos = []
        self.suspendidos = []
        self.terminados = []

    def agregar_nuevo(self, proceso: Proceso):
        # Agrega un proceso a la cola de nuevos, ordenado por tiempo de arribo.
        self.nuevos.append(proceso)
        self.nuevos.sort(key=lambda p: p.tiempo_arribo)

    def mover_nuevo_a_listo(self, proceso: Proceso):
        # Mueve un proceso de la cola de nuevos a la de listos.
        try:
            self.nuevos.remove(proceso)
            proceso.estado = "Listo"
            self.listos.append(proceso)
            self.ordenar_listos_srtf()
        except ValueError:
            print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de nuevos.")

    def mover_suspendido_a_listo(self, proceso: Proceso):
        # Mueve un proceso de la cola de suspendidos a la de listos.
        try:
            self.suspendidos.remove(proceso)
            proceso.estado = "Listo"
            self.listos.append(proceso)
            self.ordenar_listos_srtf()
        except ValueError:
            print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de suspendidos.")
            
    def mover_nuevo_a_suspendido(self, proceso: Proceso):
        # Mueve un proceso de nuevos a suspendidos cuando no hay memoria disponible.
        try:
            self.nuevos.remove(proceso)
            proceso.estado = "Listo y Suspendido"
            self.suspendidos.append(proceso)
        except ValueError:
            print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de nuevos.")

    def ordenar_listos_srtf(self):
        # Ordena la cola de listos según el tiempo restante para el algoritmo SRTF.
        self.listos.sort(key=lambda p: p.tiempo_restante)