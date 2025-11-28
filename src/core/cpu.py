from typing import Optional
from .proceso import Proceso

class CPU:
    """
    Representa la Unidad Central de Procesamiento (CPU).
    Gestiona el proceso que se está ejecutando actualmente.
    """
    def __init__(self):
        self.proceso_actual: Optional[Proceso] = None

    def dispatch(self, proceso: Proceso):
        # Asigna un proceso a la CPU para su ejecución.
        self.proceso_actual = proceso
        self.proceso_actual.estado = "Ejecucion"

    def ejecutar_ciclo(self):
        # Simula un ciclo de reloj de la CPU, decrementando el tiempo restante del proceso.
        if self.proceso_actual:
            self.proceso_actual.tiempo_restante -= 1

    def liberar(self) -> Optional[Proceso]:
        # Libera la CPU, devolviendo el proceso que estaba en ejecución.
        proceso_liberado = self.proceso_actual
        self.proceso_actual = None
        return proceso_liberado

    def esta_libre(self) -> bool:
        # Verifica si la CPU está ociosa.
        return self.proceso_actual is None

    def get_proceso_actual(self) -> Optional[Proceso]:
        # Devuelve el proceso que se encuentra actualmente en la CPU.
        return self.proceso_actual