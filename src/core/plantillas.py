from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING
from .proceso import Proceso
from .particion import Particion

if TYPE_CHECKING:
    from .colas import GestorColas
from .cpu import CPU

class GestorMemoria(ABC):
    def __init__(self):
        self.particiones = []
        # - 100K para Sistema Operativo (no disponible para procesos)
        # - 250K para trabajos grandes
        # - 150K para trabajos medianos  
        # - 50K para trabajos pequeños
        # - Calcular direcciones de inicio apropiadas
        self.inicializar_particiones()
    
    def inicializar_particiones(self):
        tams = [250, 150, 50] # tamaños de particiones
        id=0
        ult_dir = 0

        # partición e asignación del SO
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

    # Es solo el algoritmo puro 
    @abstractmethod
    def encontrar_particion(self, tamaño_proceso):
        pass
    
    # Utiliza encontrar_particion para tomar la decision y aplica los cambios en memoria
    def asignar_memoria(self, proceso: Proceso) -> (bool, Optional[str]):
        if self.hay_libre():
            particion_id = self.encontrar_particion(proceso.tamaño)
            if particion_id is not False:
                for particion in self.particiones:
                    if particion.id == particion_id:
                        particion.proceso_asignado = proceso
                        particion.fragmentacion_interna = particion.tamaño - proceso.tamaño
                        return True, f"Memoria asignada al proceso {proceso.id} en la partición {particion.id}"
        return False, None

    def liberar_memoria(self, proceso: Proceso) -> List[str]:
        eventos = []
        for particion in self.particiones:
            if particion.proceso_asignado == proceso:
                particion.proceso_asignado = None
                particion.fragmentacion_interna = 0
                eventos.append(f"Memoria liberada por el proceso {proceso.id} de la partición {particion.id}")
        return eventos
        

    def mostrar_estado_memoria(self):
        # Devuelve un diccionario con los estados de cada partición
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
        grado = 0
        for particion in self.particiones:
            if particion.proceso_asignado != None:
                grado += 1
        return grado
    
    # método para saber si alguna de las particiones está libre
    def hay_libre(self)-> bool:
        for particion in self.particiones:
            if particion.esta_libre():
                return True
        return False



class Planificador(ABC):
    def __init__(self, gestor_colas: 'GestorColas', cpu: CPU):
        self.gestor_colas = gestor_colas
        self.cpu = cpu 

    @abstractmethod
    def set_verbose(self, verbose: bool):
        pass

    @abstractmethod
    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        pass

    @abstractmethod
    def ejecutar(self, tiempo_actual: int) -> Optional[str]:
        pass

    @abstractmethod
    def manejar_finalizacion(self) -> (Optional[Proceso], Optional[str]):
        pass

    def avanzar_tiempo(self):
        self.cpu.ejecutar_ciclo()

    # Métodos que deben ser implementados por el planificador concreto (SRTF)
    @abstractmethod
    def _necesita_preempcion(self) -> (bool, Optional[str]):
        pass

    @abstractmethod
    def _preemptar(self):
        pass

    @abstractmethod
    def verificar_preempcion_inmediata(self) -> Optional[str]:
        pass