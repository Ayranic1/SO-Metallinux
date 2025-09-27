from abc import ABC, abstractmethod
from typing import Optional
from .proceso import Proceso
from .colas import GestorColas

# Clase base para arrancar, si necesitas agregar mas cosas hacelo

class GestorMemoria(ABC):
    def __init__(self):
        self.particiones = []
        # TO DO: Inicializar las particiones fijas según especificación:
        # - 100K para Sistema Operativo (no disponible para procesos)
        # - 250K para trabajos grandes
        # - 150K para trabajos medianos  
        # - 50K para trabajos pequeños
        # - Calcular direcciones de inicio apropiadas
        self.inicializar_particiones()
    
    def inicializar_particiones(self):
        # TO DO: Crear e inicializar la lista de particiones
        pass
    
    # TO DO: Implementar algoritmo (en este caso BEST-FIT) para asignación de memoria
    # Es solo el algoritmo puro
    @abstractmethod
    def encontrar_particion(self, tamaño_proceso):
        pass
    
    # TO DO: Implementar método para asignar proceso a memoria
    # Utiliza encontrar_particion para tomar la decision y aplica los cambios en memoria
    def asignar_memoria(self, proceso):
        pass
    
    # TO DO: Implementar método para liberar memoria de un proceso
    def liberar_memoria(self, proceso):
        pass
    
    # TO DO: Implementar método para obtener estado de memoria
    def obtener_estado_memoria(self):
        pass
    
    # TO DO: Implementar método para verificar grado de multiprogramación
    def grado_multiprogramacion_actual(self):
        pass

class Planificador(ABC):
    def __init__(self, gestor_colas: GestorColas):
        self.gestor_colas = gestor_colas
        self.tiempo_actual = 0
    

    # Método ABSTRACTO - cada algoritmo implementa su lógica de selección
    @abstractmethod
    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        pass

    def ejecutar(self) -> Optional[Proceso]:
        pass
    
    # TO DO: Implementar método para manejar llegada de procesos
    def manejar_llegadas(self, procesos_nuevos: list):
        pass
    
    # TO DO: Implementar método para manejar finalización de proceso
    def manejar_finalizacion(self, proceso: Proceso):
        pass
    
    # TO DO: Implementar método para avanzar el tiempo de simulación
    def avanzar_tiempo(self):
        pass

    # Estos metodos son abstractos porque depende del algoritmo de planificación que se esté aplicando la necesidad de usar
    # preempción y cómo se va aplicar
    
    # Determina si se necesita preempción
    @abstractmethod
    def _necesita_preempcion(self) -> bool:
        pass
    
    # Realiza la preempción del proceso actual
    @abstractmethod
    def _preemptar(self):
        pass
    
    # TO DO: Implementar método para generar reporte estadístico
    def generar_reporte_estadistico(self) -> dict:
        pass