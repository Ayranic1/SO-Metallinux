from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING
from .proceso import Proceso
from .particion import Particion

if TYPE_CHECKING:
    from .colas import GestorColas
from .cpu import CPU

class GestorMemoria(ABC):
    """
    Clase abstracta para la gestión de memoria. Define la interfaz para la asignación
    y liberación de particiones de memoria.
    """
    def __init__(self):
        self.particiones = []
        self.inicializar_particiones()
    
    def inicializar_particiones(self):
        # Define y crea las particiones de memoria fija del sistema.
        tams = [250, 150, 50] # Tamaños en KB
        id=0
        ult_dir = 0

        # Partición reservada para el Sistema Operativo
        t=100
        particion = Particion(str(id),ult_dir, t)
        particion.proceso_asignado = Proceso('SO', t, 0, 0)
        self.particiones.append(particion)
        ult_dir+= t
        id+=1
        
        for t in tams:
            particion = Particion(str(id),ult_dir, t)
            self.particiones.append(particion)
            ult_dir+= t
            id+=1

    @abstractmethod
    def encontrar_particion(self, tamaño_proceso: int) -> Optional[str]:
        # Algoritmo para encontrar la mejor partición disponible (p. ej., Best-Fit).
        pass
    
    def asignar_memoria(self, proceso: Proceso) -> (bool, Optional[str]):
        # Asigna un proceso a una partición de memoria si encuentra una adecuada.
        if self.hay_libre():
            particion_id = self.encontrar_particion(proceso.tamaño)
            if particion_id is not False:
                for particion in self.particiones:
                    if particion.id == particion_id:
                        particion.proceso_asignado = proceso
                        particion.fragmentacion_interna = particion.tamaño - proceso.tamaño
                        return True, f"Memoria asignada al proceso {proceso.id} en la partición {particion.id}"
        return False, None

    def liberar_memoria(self, proceso: Proceso) -> (List[str], Optional[Particion]):
        # Libera la partición de memoria ocupada por un proceso.
        eventos = []
        for particion in self.particiones:
            if particion.proceso_asignado == proceso:
                particion.proceso_asignado = None
                particion.fragmentacion_interna = 0
                eventos.append(f"Memoria liberada por el proceso {proceso.id} de la partición {particion.id}")
                return eventos, particion
        return [], None
        

    def mostrar_estado_memoria(self):
        # Devuelve una representación del estado actual de la memoria.
        estado_actual = []
    
        for particion in self.particiones:
        
            if particion.proceso_asignado is None:
                estado = "Libre"
                proceso_info = "N/A"
            else:
                estado = "Ocupada"

                proceso_info = f"PID={particion.proceso_asignado.pid}, Nombre='{particion.proceso_asignado.nombre}'"
            
            registro = {
                "ID_Particion": particion.id_particion,
                "Tamaño": particion.tamano,
                "Estado": estado,
                "Proceso_Asignado": proceso_info
            }
            estado_actual.append(registro)
            
        return estado_actual
    
    def grado_multiprogramacion_actual(self):
        # Calcula el número de procesos actualmente en memoria.
        grado = 0
        for particion in self.particiones:
            if particion.proceso_asignado != None:
                grado += 1
        return grado
    
    def hay_libre(self)-> bool:
        # Verifica si hay al menos una partición libre.
        for particion in self.particiones:
            if particion.esta_libre():
                return True
        return False

    def proceso_cabe_en_particion(self, proceso: Proceso, particion: Particion) -> bool:
        # Comprueba si un proceso cabe en una partición específica.
        return particion.tamaño >= proceso.tamaño



class Planificador(ABC):
    """
    Clase abstracta para los planificadores de CPU. Define la interfaz que deben
    implementar los algoritmos de planificación concretos.
    """
    def __init__(self, gestor_colas: 'GestorColas', cpu: CPU):
        self.gestor_colas = gestor_colas
        self.cpu = cpu 

    @abstractmethod
    def set_verbose(self, verbose: bool):
        pass

    @abstractmethod
    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        # Lógica para elegir el siguiente proceso de la cola de listos.
        pass

    @abstractmethod
    def ejecutar(self, tiempo_actual: int) -> Optional[str]:
        # Asigna un proceso a la CPU si corresponde.
        pass

    @abstractmethod
    def manejar_finalizacion(self) -> (Optional[Proceso], Optional[str]):
        # Gestiona la finalización de un proceso en la CPU.
        pass

    def avanzar_tiempo(self):
        # Avanza el tiempo de la CPU en un ciclo.
        self.cpu.ejecutar_ciclo()

    @abstractmethod
    def _necesita_preempcion(self) -> (bool, Optional[str]):
        # Verifica si es necesario realizar una preempción.
        pass

    @abstractmethod
    def _preemptar(self):
        # Realiza la preempción del proceso en CPU.
        pass

    @abstractmethod
    def verificar_preempcion_inmediata(self) -> Optional[str]:
        # Comprueba y ejecuta una preempción inmediatamente.
        pass