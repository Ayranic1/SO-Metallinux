from typing import List, Optional
from .proceso import Proceso
from .plantillas import GestorMemoria, Planificador
from .colas import GestorColas
from .particion import Particion

class Kernel:
    """
    Representa el núcleo del sistema operativo, coordinando la gestión de procesos,
    memoria y el planificador.
    """
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
        # El grado de multiprogramación se define como la cantidad de procesos en Listos y Suspendidos.
        return len(self.gestor_colas.listos) + len(self.gestor_colas.suspendidos)

    def ciclo_de_trabajo(self, tiempo_actual: int) -> (Optional[Proceso], List[str]):
        """
        Ejecuta un ciclo de la simulación, manejando llegadas, finalizaciones y planificación.
        """
        eventos = []
        
        # 1. Gestionar la finalización de procesos que estaban en la CPU.
        proceso_terminado, evento_fin = self.planificador.manejar_finalizacion()
        if evento_fin:
            eventos.append(evento_fin)
        
        if proceso_terminado:
            # Si un proceso terminó, se libera su memoria y se intenta asignar a otros.
            eventos_liberacion, particion_liberada = self.gestor_memoria.liberar_memoria(proceso_terminado)
            eventos.extend(eventos_liberacion)
            eventos.extend(self._intentar_asignar_memoria(particion_liberada))
            
            # Se intenta despachar un nuevo proceso a la CPU inmediatamente.
            evento_ejecucion = self.planificador.ejecutar(tiempo_actual)
            if evento_ejecucion:
                eventos.append(evento_ejecucion)

            return proceso_terminado, eventos

        # 2. Intentar asignar memoria si no hubo finalizaciones.
        eventos.extend(self._intentar_asignar_memoria())

        # 3. Ejecutar el planificador para despachar un proceso si la CPU está libre.
        evento_ejecucion = self.planificador.ejecutar(tiempo_actual)
        if evento_ejecucion:
            eventos.append(evento_ejecucion)

        # 4. Avanzar el reloj de la CPU.
        self.planificador.avanzar_tiempo()
        
        return None, eventos

    def _manejar_llegadas(self, tiempo_actual: int) -> List[str]:
        eventos = []
        # Revisa la lista maestra de procesos para ver si alguno llega en el tiempo actual.
        for proceso in self.procesos_maestros:
            if proceso.tiempo_arribo == tiempo_actual:
                eventos.append(f"Llega el proceso {proceso.id} (Tamaño: {proceso.tamaño}K, Irrupción: {proceso.tiempo_irrupcion})")
                self.gestor_colas.agregar_nuevo(proceso)
                self.procesos_maestros.remove(proceso)
        return eventos

    def _intentar_asignar_memoria(self, particion_liberada: Optional[Particion] = None) -> List[str]:
        """
        Intenta asignar memoria a procesos en espera, con una lógica de prioridades.
        Si se especifica una partición, se le da prioridad para la asignación.
        """
        eventos = []
        
        if particion_liberada:
            # Prioridad 1: Procesos en Listos y Suspendidos que quepan en la partición liberada.
            for proceso in self.gestor_colas.suspendidos:
                if self.gestor_memoria.proceso_cabe_en_particion(proceso, particion_liberada):
                    asignado, evento = self.gestor_memoria.asignar_memoria(proceso)
                    if asignado:
                        self.gestor_colas.mover_suspendido_a_listo(proceso)
                        eventos.append(f"Proceso {proceso.id} reanudado y movido a Listos. (DOM: {self._get_current_dom()})")
                        
                        if self._get_current_dom() < 5 and self.gestor_colas.nuevos:
                            proceso_nuevo = self.gestor_colas.nuevos[0]
                            self.gestor_colas.mover_nuevo_a_suspendido(proceso_nuevo)
                            eventos.append(f"Proceso {proceso_nuevo.id} ingresa a Listos y Suspendidos. (DOM: {self._get_current_dom()})")

                        evento_preempcion = self.planificador.verificar_preempcion_inmediata()
                        if evento_preempcion:
                            eventos.append(evento_preempcion)
                        return eventos

            # Prioridad 2: Procesos Nuevos que quepan en la partición liberada.
            if self._get_current_dom() < 5:
                for proceso in self.gestor_colas.nuevos:
                     if self.gestor_memoria.proceso_cabe_en_particion(proceso, particion_liberada):
                        asignado, evento = self.gestor_memoria.asignar_memoria(proceso)
                        if asignado:
                            self.gestor_colas.mover_nuevo_a_listo(proceso)
                            eventos.append(f"Memoria asignada al proceso {proceso.id}. Movido a Listos. (DOM: {self._get_current_dom()})")
                            
                            evento_preempcion = self.planificador.verificar_preempcion_inmediata()
                            if evento_preempcion:
                                eventos.append(evento_preempcion)
                            return eventos
            return eventos

        # Lógica general si no se liberó una partición específica.
        # Intenta asignar memoria a procesos suspendidos o nuevos en cualquier partición disponible.
        for proceso in self.gestor_colas.suspendidos[:]:
            asignado, evento = self.gestor_memoria.asignar_memoria(proceso)
            if asignado:
                self.gestor_colas.mover_suspendido_a_listo(proceso)
                eventos.append(f"Proceso {proceso.id} reanudado y movido a Listos. (DOM: {self._get_current_dom()})")
                
                evento_preempcion = self.planificador.verificar_preempcion_inmediata()
                if evento_preempcion:
                    eventos.append(evento_preempcion)
                return eventos
        
        for proceso in self.gestor_colas.nuevos[:]:
            if self._get_current_dom() >= 5:
                break 

            asignado, evento = self.gestor_memoria.asignar_memoria(proceso)
            if asignado:
                self.gestor_colas.mover_nuevo_a_listo(proceso)
                eventos.append(f"Memoria asignada al proceso {proceso.id}. Movido a Listos. (DOM: {self._get_current_dom()})")

                evento_preempcion = self.planificador.verificar_preempcion_inmediata()
                if evento_preempcion:
                    eventos.append(evento_preempcion)
                return eventos
            else:
                if self._get_current_dom() < 5:
                    self.gestor_colas.mover_nuevo_a_suspendido(proceso)
                    eventos.append(f"Proceso {proceso.id} no cabe en memoria. Movido a Listos y Suspendidos. (DOM: {self._get_current_dom()})")
        return eventos