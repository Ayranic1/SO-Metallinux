from typing import Optional
from .proceso import Proceso
from .colas import GestorColas
from .plantillas import Planificador
from .cpu import CPU

class PlanificadorSRTF(Planificador):
    def __init__(self, gestor_colas: GestorColas, cpu: CPU):
        super().__init__(gestor_colas, cpu)

    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        if not self.gestor_colas.listos:
            return None

        # Encuentra y devuelve el proceso con el mínimo tiempo restante
        proceso_seleccionado = min(self.gestor_colas.listos, key=lambda p: p.tiempo_restante)
        return proceso_seleccionado

    def _necesita_preempcion(self) -> bool:
        proceso_en_cpu = self.cpu.get_proceso_actual()
        if proceso_en_cpu is None or not self.gestor_colas.listos:
            return False

        mejor_proceso_listo = self.seleccionar_proximo_proceso_listo()
        
        if mejor_proceso_listo.tiempo_restante < proceso_en_cpu.tiempo_restante:
            print(f"PREEMPCIÓN: Proceso {mejor_proceso_listo.id} (t={mejor_proceso_listo.tiempo_restante}) desaloja a {proceso_en_cpu.id} (t={proceso_en_cpu.tiempo_restante})")
            return True
        return False

    def _preemptar(self):
        proceso_desalojado = self.cpu.liberar() 
        if proceso_desalojado:
            proceso_desalojado.estado = "Listo"
            self.gestor_colas.listos.append(proceso_desalojado)