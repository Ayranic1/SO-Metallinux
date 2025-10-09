# cpu.py

from typing import Optional
from .proceso import Proceso

class CPU:
    def __init__(self):
        self.proceso_actual: Optional[Proceso] = None

    def dispatch(self, proceso: Proceso):
        self.proceso_actual = proceso
        self.proceso_actual.estado = "Ejecucion"

    def ejecutar_ciclo(self) -> Optional[Proceso]:
        if self.proceso_actual:
            self.proceso_actual.tiempo_restante -= 1
            return self.proceso_actual
        return None

    def liberar(self) -> Optional[Proceso]:
        proceso_liberado = self.proceso_actual
        self.proceso_actual = None
        return proceso_liberado

    def esta_libre(self) -> bool:
        return self.proceso_actual is None

    def get_proceso_actual(self) -> Optional[Proceso]:
        return self.proceso_actual