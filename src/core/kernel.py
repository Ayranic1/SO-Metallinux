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
        
    def _get_current_dom(self) -> int:
        # Calcula el Grado de Multiprogramación(DOM): Listos + Listos y Suspendidos.
        # El límite de 5 procesos activos es entre ambas colas, excluyendo Nuevos y Terminados.
        return len(self.gestor_colas.listos) + len(self.gestor_colas.suspendidos)

    def ciclo_de_trabajo(self, tiempo_actual: int) -> Optional[Proceso]:
        # 1. Manejar las llegadas de nuevos procesos (van a la cola de Nuevos)
        self._manejar_llegadas(tiempo_actual)

        # 2. Manejar la finalización del proceso en CPU (si aplica)
        proceso_terminado = self.planificador.manejar_finalizacion()
        if proceso_terminado:
            self.gestor_memoria.liberar_memoria(proceso_terminado)
            
            # Intentar asignar memoria inmediatamente tras la liberación.
            self._intentar_asignar_memoria() 
            return proceso_terminado

        # 3. Intentar asignar memoria a procesos suspendidos/nuevos 
        self._intentar_asignar_memoria()

        # 4. Ejecutar el planificador/CPU
        proceso_en_cpu = self.planificador.ejecutar()
        if proceso_en_cpu:
            print(f"Proceso en CPU: {proceso_en_cpu.id} (Restante: {proceso_en_cpu.tiempo_restante})")
        else:
            print("CPU Ociosa")

        # 5. Avanzar el tiempo (ejecutar ciclo de CPU)
        self.planificador.avanzar_tiempo()
        
        return None

    def _manejar_llegadas(self, tiempo_actual: int):
        for proceso in self.procesos_maestros:
            if proceso.tiempo_arribo == tiempo_actual:
                print(f"Llega el proceso {proceso.id} (Tamaño: {proceso.tamaño}K, Irrupción: {proceso.tiempo_irrupcion})")
                # Los procesos que llegan pasan a Nuevos, donde esperan la admisión al DOM.
                self.gestor_colas.agregar_nuevo(proceso)

    def _intentar_asignar_memoria(self):
        
        # Prioridad 1: Procesos Listos y Suspendidos
        # Se prioriza reanudar procesos que ya están en el DOM.
        for proceso in self.gestor_colas.suspendidos[:]:
            if self.gestor_memoria.asignar_memoria(proceso):
                self.gestor_colas.mover_suspendido_a_listo(proceso)
                print(f"Proceso {proceso.id} reanudado y movido a Listos. (DOM: {self._get_current_dom()})")
                # Re-evaluar inmediatamente después de reanudar un proceso.
                return self._intentar_asignar_memoria() 
        
        # Prioridad 2: Procesos Nuevos
        for proceso in self.gestor_colas.nuevos[:]:
            
            # Criterio 1: Verificar el Grado de Multiprogramación (DOM <= 5)
            if self._get_current_dom() >= 5:
                print(f"Proceso {proceso.id} (Nuevo) espera: Grado de Multiprogramación ({self._get_current_dom()}) al límite (5).")
                # Si el DOM está al límite, los nuevos deben esperar en la cola de nuevos.
                break 

            # Criterio 2: Intentar asignar memoria (Best-Fit)
            if self.gestor_memoria.asignar_memoria(proceso):
                # Caso A: Cabe en la memoria. Va a Listos.
                self.gestor_colas.mover_nuevo_a_listo(proceso)
                print(f"Memoria asignada al proceso {proceso.id}. Movido a Listos. (DOM: {self._get_current_dom()})")
                # Re-evaluar inmediatamente después de admitir un proceso.
                return self._intentar_asignar_memoria()
            else:
                # Caso B: No cabe en la memoria, pero DOM < 5. Debe ser admitido al DOM y pasar a Suspendidos.
                self.gestor_colas.mover_nuevo_a_suspendido(proceso)
                print(f"Proceso {proceso.id} no cabe en memoria. Movido a Listos y Suspendidos. (DOM: {self._get_current_dom()})")
                # Al mover a suspendidos, se continúa revisando si otros procesos nuevos caben en alguna partición.