# Clase base para arrancar, si necesitas agregar mas cosas hacelo

from typing import Optional
from .proceso import Proceso
from .colas import GestorColas

class PlanificadorSRTF:
    def __init__(self, gestor_colas: GestorColas):
        self.gestor_colas = gestor_colas
        self.tiempo_actual = 0
    
    # TO DO: Implementar el algoritmo SRTF (Shortest Remaining Time First)
    # - Si no hay proceso en ejecución, asignar el de menor tiempo_restante
    # - Si hay proceso en ejecución, verificar si necesita preempción
    # - Manejar los casos de llegada de nuevos procesos
    def ejecutar_srtf(self) -> Optional[Proceso]:
        pass
    
    # TO DO: Implementar método para manejar llegada de procesos
    def manejar_llegadas(self, procesos_nuevos: list):
        pass
    
    # TO DO: Implementar método para manejar finalización de proceso
    def manejar_finalizacion(self, proceso: Proceso):
        pass
    
    # TO DO: Implementar método para verificar eventos en tiempo actual
    def obtener_eventos_actuales(self) -> list:
        pass
    
    # TO DO: Implementar método para avanzar el tiempo de simulación
    def avanzar_tiempo(self):
        pass
    
    # TO DO: Implementar método para preemptar proceso actual
    def preemptar(self) -> bool:
        pass
    
    # TO DO: Implementar método para calcular próximo tiempo de evento
    def proximo_evento_tiempo(self) -> int:
        pass
    
    # TO DO: Implementar método para generar reporte estadístico
    def generar_reporte_estadistico(self) -> dict:
        pass