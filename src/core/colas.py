# Clase base para arrancar, si necesitas agregar mas cosas hacelo

from .proceso import Proceso
from core.gestor_memoriaBestFit import GestorMemoriaBestFit as gm

class GestorColas:
    def __init__(self):
        # TO DO: Inicializar las colas de estados
        self.nuevos = []          # Procesos que aún no han llegado
        self.listos = []          # Procesos en memoria esperando CPU
        self.suspendidos = []     # Procesos listos pero sin memoria
        self.ejecucion = None     # Proceso actual en CPU (solo uno)
        self.terminados = []      # Procesos que finalizaron
        
        # TO DO: Inicializar contadores para estadísticas
        self.tiempo_total_espera = 0
        self.procesos_completados = 0
    
    # TO DO: Implementar método para agregar proceso a cola de nuevos
    # - Ordenar por tiempo de arribo 
    def agregar_nuevo(self, proceso: Proceso):
        '''
            Agrega y ordena la lista de mayor a menor tiempo de irrupción.
        '''
        self.nuevos.append(proceso)
        self.nuevos.sort(key=lambda proceso: proceso.tiempo_irrupcion, reverse=True)
        
    
    # TO DO: Implementar método para mover proceso de nuevos a listos
    def nuevo_a_listo(self, proceso: Proceso, GestorMemoria: gm):
        '''
            Toma el proceso y lo saca de la cola de nuevos y lo pone en la cola de listos
        '''
        if GestorMemoria.hay_libre():
            id = GestorMemoria.encontrar_particion(proceso.tamaño)
            if id != False:
                self.listos.append(proceso)
                gm.asignar_memoria(proceso)
                try:
                    self.nuevos.remove(proceso)
                except ValueError:
                    print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de nuevos.")
                    return False
                return True
        return False
    
    # TO DO: Implementar método para mover proceso a suspendidos
    def a_suspendidos(self, proceso: Proceso):
        '''
            Agrega el proceso a la cola de suspendidos.
        '''
        self.ejecucion.estado = "Suspendido"
        self.suspendidos.append(self.ejecucion)
        self.ejecucion = None
        
    
    # TO DO: Implementar método para activar proceso suspendido
    # - Mover de suspendidos a listos si hay memoria disponible
    def activar_suspendido(self, proceso: Proceso, GestorMemoria: gm):
        '''
            Toma el proceso y lo saca de la cola de suspendidos y lo pone en la cola de listos
        '''
        if GestorMemoria.hay_libre():
            id = GestorMemoria.encontrar_particion(proceso.tamaño)
            if id != False:
                self.listos.append(proceso)
                gm.asignar_memoria(proceso)
                try:
                    self.suspendidos.remove(proceso)
                except ValueError:
                    print(f"ERROR: El proceso {proceso.id} no se encontró en la cola de suspendidos.")
                    return False
                return True
        return False


    # TO DO: Implementar método para asignar CPU a proceso
    def asignar_cpu(self, proceso: Proceso):
        self.a_suspendidos(self.ejecucion)
        self.ejecucion = proceso
    
    # TO DO: Implementar método para liberar CPU
    def liberar_cpu(self, terminado: bool = True):
        self.ejecucion.estado = "Terminado"
        self.terminados.append(self.ejecucion)
        self.ejecucion = None
