#  Definición básica para arrancar, después lo cambiamos

from .cpu import CPU
from .gestor_memoriaBestFit import GestorMemoriaBestFit
from .planificadorSRTF import PlanificadorSRTF
from .colas import GestorColas
from .proceso import Proceso
from typing import List

class Simulador:
    def __init__(self, procesos: List[Proceso]):
        self.reloj = 0
        self.procesos_maestros = procesos  # Lista completa de procesos a simular
        self.cpu = CPU()
        self.gestor_memoria = GestorMemoriaBestFit()
        self.gestor_colas = GestorColas()
        self.planificador = PlanificadorSRTF(self.gestor_colas)
        self.estadisticas = {
            'tiempos_retorno': {},
            'tiempos_espera': {},
            'uso_cpu': 0,
            'procesos_terminados': 0,
            'tiempo_final': 0,
        }

    def run(self):
        """Bucle principal que orquesta la simulación ciclo a ciclo."""
        print("--- Iniciando Simulación ---")
        # El bucle se ejecuta mientras haya procesos encolados o por llegar
        while not self._simulacion_finalizada():
            print(f"\n--- Ciclo {self.reloj} ---")

            self.planificador.manejar_llegadas(self.procesos_maestros)

            self._intentar_asignar_memoria()

            proceso_terminado = self.planificador.manejar_finalizacion()
            if proceso_terminado:
                self._registrar_estadisticas_finalizacion(proceso_terminado)
                self.gestor_memoria.liberar_memoria(proceso_terminado)

            proceso_en_cpu = self.planificador.ejecutar()
            if proceso_en_cpu:
                self.estadisticas['uso_cpu'] += 1
                print(f"Proceso en CPU: {proceso_en_cpu.id} (Restante: {proceso_en_cpu.tiempo_restante})")
            else:
                print("CPU Ociosa")

            self.planificador.avanzar_tiempo()
            self.reloj += 1

        print(f"\n--- Simulación Finalizada en tiempo {self.reloj} ---")
        self.estadisticas['tiempo_final'] = self.reloj

    def _intentar_asignar_memoria(self):
        # TO DO: Implementar la lógica para mover procesos de la cola de nuevos y suspendidos
        # a la cola de listos, asignándoles memoria con el gestor_memoria.
        # Debería priorizar los procesos suspendidos sobre los nuevos.
        pass

    def _simulacion_finalizada(self) -> bool:
        """Verifica si la simulación ha terminado."""
        total_procesos = len(self.procesos_maestros)
        procesos_terminados = len(self.gestor_colas.terminados)
        return total_procesos == procesos_terminados

    def _registrar_estadisticas_finalizacion(self, proceso: Proceso):
        tiempo_retorno = self.reloj - proceso.tiempo_arribo
        tiempo_espera = tiempo_retorno - proceso.tiempo_irrupcion
        
        self.estadisticas['tiempos_retorno'][proceso.id] = tiempo_retorno
        self.estadisticas['tiempos_espera'][proceso.id] = tiempo_espera
        self.estadisticas['procesos_terminados'] += 1

    def generar_reporte_estadistico(self) -> dict:
        print("\n--- Reporte Estadístico ---")
        num_terminados = self.estadisticas['procesos_terminados']
        if num_terminados == 0:
            reporte = {
                "Tiempo promedio de retorno": 0,
                "Tiempo promedio de espera": 0,
                "Uso de CPU (%)": 0
            }
        else:
            total_retorno = sum(self.estadisticas['tiempos_retorno'].values())
            total_espera = sum(self.estadisticas['tiempos_espera'].values())
            tiempo_final = self.estadisticas['tiempo_final']
            uso_cpu_porcentaje = (self.estadisticas['uso_cpu'] / tiempo_final) * 100 if tiempo_final > 0 else 0
            reporte = {
                "Tiempo promedio de retorno": total_retorno / num_terminados,
                "Tiempo promedio de espera": total_espera / num_terminados,
                "Uso de CPU (%)": uso_cpu_porcentaje
            }
        
        for key, value in reporte.items():
            print(f"{key}: {value:.2f}")
        return reporte
