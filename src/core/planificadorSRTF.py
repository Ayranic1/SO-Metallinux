# Clase base para arrancar, si necesitas agregar mas cosas hacelo
from abc import ABC, abstractmethod
from typing import Optional
from .proceso import Proceso
from .colas import GestorColas
from .interfaces import Planificador

class PlanificadorSRTF(Planificador):
    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        pass

        # Determina si se necesita preempción
    def _necesita_preempcion(self) -> bool:
        pass
    
    # Realiza la preempción del proceso actual
    def _preemptar(self):
        pass

