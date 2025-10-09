from typing import Optional
from .proceso import Proceso
from .colas import GestorColas
from .plantillas import Planificador

class PlanificadorSRTF(Planificador):
    def __init__(self, gestor_colas: GestorColas):
        super().__init__(gestor_colas)

    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        if not self.gestor_colas.listos:
            return None

        # Encuentra y devuelve el proceso con el mínimo tiempo restante
        proceso_seleccionado = min(self.gestor_colas.listos, key=lambda p: p.tiempo_restante)
        return proceso_seleccionado

    def _necesita_preempcion(self) -> bool:
        # No hay preempción si la CPU está libre o no hay nadie en la cola de listos
        if self.gestor_colas.ejecucion is None or not self.gestor_colas.listos:
            return False

        # Encuentra al mejor candidato de la cola de listos
        mejor_proceso_listo = self.seleccionar_proximo_proceso_listo()

        # Compara el tiempo restante del proceso en ejecución con el mejor de la cola de listos
        if mejor_proceso_listo.tiempo_restante < self.gestor_colas.ejecucion.tiempo_restante:
            print(f"PREEMPCIÓN: Proceso {mejor_proceso_listo.id} (t={mejor_proceso_listo.tiempo_restante}) desaloja a {self.gestor_colas.ejecucion.id} (t={self.gestor_colas.ejecucion.tiempo_restante})")
            return True

        return False

    def _preemptar(self):
        if self.gestor_colas.ejecucion:
            proceso_desalojado = self.gestor_colas.ejecucion
            proceso_desalojado.estado = "Listo"
            self.gestor_colas.listos.append(proceso_desalojado)
            self.gestor_colas.ejecucion = None