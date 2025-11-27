from typing import List, Optional
from .proceso import Proceso
from .plantillas import GestorMemoria, Planificador
from .colas import GestorColas

class Kernel:
    def __init__(
        self,
        procesos_maestros: List[Proceso],
        gestor_memoria: GestorMemoria,
        planificador: Planificador,
        gestor_colas: GestorColas,
        verbose: bool = True
    ):
        self.procesos_maestros = procesos_maestros
        self.gestor_memoria = gestor_memoria
        self.planificador = planificador
        self.gestor_colas = gestor_colas
        self.verbose = verbose
        self.planificador.set_verbose(verbose)
        
    def _get_current_dom(self) -> int:
        # Calcula el Grado de Multiprogramación(DOM): Listos + Listos y Suspendidos.
        return len(self.gestor_colas.listos) + len(self.gestor_colas.suspendidos)

    def ciclo_de_trabajo(self, tiempo_actual: int) -> (Optional[Proceso], List[str]):
        eventos = []
        
        # 1. Manejar llegadas
        eventos.extend(self._manejar_llegadas(tiempo_actual))

        # 2. Manejar finalización
        proceso_terminado, evento_fin = self.planificador.manejar_finalizacion()
        if evento_fin:
            eventos.append(evento_fin)
        
        if proceso_terminado:
            eventos.extend(self.gestor_memoria.liberar_memoria(proceso_terminado))
            eventos.extend(self._intentar_asignar_memoria())
            return proceso_terminado, eventos

        # 3. Asignar memoria
        eventos.extend(self._intentar_asignar_memoria())

        # 4. Ejecutar planificador
        evento_ejecucion = self.planificador.ejecutar(tiempo_actual)
        if evento_ejecucion:
            eventos.append(evento_ejecucion)

        # 5. Avanzar tiempo
        self.planificador.avanzar_tiempo()
        
        return None, eventos

    def _manejar_llegadas(self, tiempo_actual: int) -> List[str]:
        eventos = []
        for proceso in self.procesos_maestros:
            if proceso.tiempo_arribo == tiempo_actual:
                eventos.append(f"Llega el proceso {proceso.id} (Tamaño: {proceso.tamaño}K, Irrupción: {proceso.tiempo_irrupcion})")
                self.gestor_colas.agregar_nuevo(proceso)
                self.procesos_maestros.remove(proceso)
        return eventos

    def _intentar_asignar_memoria(self) -> List[str]:
        eventos = []
        # Prioridad 1: Procesos Suspendidos
        for proceso in self.gestor_colas.suspendidos[:]:
            asignado, evento = self.gestor_memoria.asignar_memoria(proceso)
            if asignado:
                self.gestor_colas.mover_suspendido_a_listo(proceso)
                eventos.append(f"Proceso {proceso.id} reanudado y movido a Listos. (DOM: {self._get_current_dom()})")
                
                # Verificar preempción inmediata
                evento_preempcion = self.planificador.verificar_preempcion_inmediata()
                if evento_preempcion:
                    eventos.append(evento_preempcion)
                
                eventos.extend(self._intentar_asignar_memoria())
                return eventos
        
        # Prioridad 2: Procesos Nuevos
        for proceso in self.gestor_colas.nuevos[:]:
            if self._get_current_dom() >= 5:
                eventos.append(f"Proceso {proceso.id} (Nuevo) espera: Grado de Multiprogramación ({self._get_current_dom()}) al límite (5).")
                break 

            asignado, evento = self.gestor_memoria.asignar_memoria(proceso)
            if asignado:
                self.gestor_colas.mover_nuevo_a_listo(proceso)
                eventos.append(f"Memoria asignada al proceso {proceso.id}. Movido a Listos. (DOM: {self._get_current_dom()})")

                # Verificar preempción inmediata
                evento_preempcion = self.planificador.verificar_preempcion_inmediata()
                if evento_preempcion:
                    eventos.append(evento_preempcion)

                eventos.extend(self._intentar_asignar_memoria())
                return eventos
            else:
                self.gestor_colas.mover_nuevo_a_suspendido(proceso)
                eventos.append(f"Proceso {proceso.id} no cabe en memoria. Movido a Listos y Suspendidos. (DOM: {self._get_current_dom()})")
        return eventos