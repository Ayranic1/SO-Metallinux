from .proceso import Proceso

class GestorColas:
    def __init__(self):
        self.nuevos = []
        self.listos = []
        self.suspendidos = []
        self.ejecucion = None
        self.terminados = []
        self.tiempo_total_espera = 0
        self.procesos_completados = 0

    def agregar_nuevo(self, proceso: Proceso):
        self.nuevos.append(proceso)
        self.nuevos.sort(key=lambda p: p.tiempo_arribo)

    def mover_nuevo_a_listo(self, proceso: Proceso):
        try:
            self.nuevos.remove(proceso)
            proceso.estado = "Listo"
            self.listos.append(proceso)
            # Ordenar por tiempo restante (SRTF)
            self.listos.sort(key=lambda p: p.tiempo_restante)
        except ValueError:
            print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de nuevos.")

    def mover_suspendido_a_listo(self, proceso: Proceso):
        try:
            self.suspendidos.remove(proceso)
            proceso.estado = "Listo"
            self.listos.append(proceso)
            # Ordenar por tiempo restante (SRTF)
            self.listos.sort(key=lambda p: p.tiempo_restante)
        except ValueError:
            print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de suspendidos.")
            
    def mover_nuevo_a_suspendido(self, proceso: Proceso):
        # Mueve un proceso de la cola de nuevos a la cola de listos y suspendidos, si no cabe en memoria.
        try:
            self.nuevos.remove(proceso)
            proceso.estado = "Listo y Suspendido"
            self.suspendidos.append(proceso)
        except ValueError:
            print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de nuevos.")

    def ordenar_listos_srtf(self):
        self.listos.sort(key=lambda p: p.tiempo_restante)