# Clase básica para empezar

from typing import Optional
from .proceso import Proceso


class CPU:
    def __init__(self):
        self.proceso_actual: Optional[Proceso] = None

    def dispatch(self, proceso: Proceso):
        # TO DO: Asignar un proceso a la CPU para su ejecución (dispatching).
        pass

    def ejecutar_ciclo(self) -> Optional[Proceso]:
        # To DO: Simula un ciclo de reloj de la CPU.
        pass

    def liberar(self) -> Optional[Proceso]:
        # TO DO:: Libera la CPU del proceso actual
        pass

    def esta_libre(self) -> bool:
        return self.proceso_actual is None

    def get_proceso_actual(self) -> Optional[Proceso]:
        return self.proceso_actual