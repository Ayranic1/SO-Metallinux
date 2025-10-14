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
        gestor_colas: GestorColas
    ):
        self.procesos_maestros = procesos_maestros
        self.gestor_memoria = gestor_memoria
        self.planificador = planificador
        self.gestor_colas = gestor_colas

    def ciclo_de_trabajo(self, tiempo_actual: int) -> Optional[Proceso]:
        self._manejar_llegadas(tiempo_actual)

        self._intentar_asignar_memoria()

        proceso_terminado = self.planificador.manejar_finalizacion()
        if proceso_terminado:
            self.gestor_memoria.liberar_memoria(proceso_terminado)
            return proceso_terminado

        proceso_en_cpu = self.planificador.ejecutar()
        if proceso_en_cpu:
            print(f"Proceso en CPU: {proceso_en_cpu.id} (Restante: {proceso_en_cpu.tiempo_restante})")
        else:
            print("CPU Ociosa")

        self.planificador.avanzar_tiempo()
        
        return None

    def _manejar_llegadas(self, tiempo_actual: int):
        for proceso in self.procesos_maestros:
            if proceso.tiempo_arribo == tiempo_actual:
                print(f"Llega el proceso {proceso.id} (Tamaño: {proceso.tamaño}K, Irrupción: {proceso.tiempo_irrupcion})")
                self.gestor_colas.agregar_nuevo(proceso)

    def _intentar_asignar_memoria(self):
        # TO DO: La lógica de multiprogramación se implementaría aquí.
        # Por ahora, se asigna si hay cualquier partición libre.

        # Prioridad 1: Procesos listos pero suspendidos
        for proceso in self.gestor_colas.suspendidos[:]: # Iterar sobre una copia
            if self.gestor_memoria.asignar_memoria(proceso):
                self.gestor_colas.mover_suspendido_a_listo(proceso)
                print(f"Proceso {proceso.id} reanudado y movido a Listos.")

        # Prioridad 2: Procesos nuevos
        for proceso in self.gestor_colas.nuevos[:]: # Iterar sobre una copia
            if self.gestor_memoria.asignar_memoria(proceso):
                self.gestor_colas.mover_nuevo_a_listo(proceso)
                print(f"Memoria asignada al proceso {proceso.id}. Movido a Listos.")