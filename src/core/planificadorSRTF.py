from typing import Optional
from .proceso import Proceso
from .colas import GestorColas
from .plantillas import Planificador
from .cpu import CPU

class PlanificadorSRTF(Planificador):
    def __init__(self, gestor_colas: GestorColas, cpu: CPU):
        super().__init__(gestor_colas, cpu)
        self.verbose = True

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        if not self.gestor_colas.listos:
            return None
        return min(self.gestor_colas.listos, key=lambda p: p.tiempo_restante)

    def _necesita_preempcion(self) -> (bool, Optional[str]):
        proceso_en_cpu = self.cpu.get_proceso_actual()
        if proceso_en_cpu is None or not self.gestor_colas.listos:
            return False, None

        mejor_proceso_listo = self.seleccionar_proximo_proceso_listo()
        
        if mejor_proceso_listo.tiempo_restante < proceso_en_cpu.tiempo_restante:
            evento = f"PREEMPCIÓN: Proceso {mejor_proceso_listo.id} (t={mejor_proceso_listo.tiempo_restante}) desaloja a {proceso_en_cpu.id} (t={proceso_en_cpu.tiempo_restante})"
            return True, evento
        return False, None

    def _preemptar(self):
        proceso_desalojado = self.cpu.liberar()
        if proceso_desalojado:
            proceso_desalojado.estado = "Listo"
            self.gestor_colas.listos.append(proceso_desalojado)

    def ejecutar(self, tiempo_actual: int) -> Optional[str]:
        if self.cpu.esta_libre():
            proximo_proceso = self.seleccionar_proximo_proceso_listo()
            if proximo_proceso:
                self.cpu.dispatch(proximo_proceso)
                self.gestor_colas.listos.remove(proximo_proceso)
                return f"Tiempo {tiempo_actual}: Se asigna CPU al proceso {proximo_proceso.id} (Restante: {proximo_proceso.tiempo_restante})"
        
        return None

    def manejar_finalizacion(self) -> (Optional[Proceso], Optional[str]):
        if not self.cpu.esta_libre() and self.cpu.get_proceso_actual().tiempo_restante <= 0:
            proceso_terminado = self.cpu.liberar()
            proceso_terminado.estado = "Terminado"
            self.gestor_colas.terminados.append(proceso_terminado)
            return proceso_terminado, f"Proceso {proceso_terminado.id} ha terminado."
        return None, None

    def verificar_preempcion_inmediata(self) -> Optional[str]:
        necesita_preempcion, evento_preempcion = self._necesita_preempcion()
        if necesita_preempcion:
            self._preemptar()
            return evento_preempcion
        return None