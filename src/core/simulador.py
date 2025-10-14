from typing import List
from .proceso import Proceso
from .cpu import CPU
from .colas import GestorColas
from .gestor_memoriaBestFit import GestorMemoriaBestFit
from .planificadorSRTF import PlanificadorSRTF
from .kernel import Kernel

class Simulador:
    def __init__(self, procesos: List[Proceso]):
        self.reloj = 0
        self.procesos_maestros = procesos

        # 1. Crear todos los componentes del sistema
        cpu = CPU()
        gestor_colas = GestorColas()
        gestor_memoria = GestorMemoriaBestFit()
        planificador = PlanificadorSRTF(gestor_colas, cpu)
        
        # 2. Inyectar dependencias en el Kernel
        self.kernel = Kernel(
            self.procesos_maestros,
            gestor_memoria,
            planificador,
            gestor_colas
        )
        
        # 3. Contenedor de estadísticas
        self.estadisticas = {
            'tiempos_retorno': {},
            'tiempos_espera': {},
            'uso_cpu': 0,
            'tiempo_final': 0,
        }

    def run(self):
        print("--- Iniciando Simulación ---")
        
        while not self._simulacion_finalizada():
            print(f"\n--- Ciclo {self.reloj} ---")

            proceso_terminado = self.kernel.ciclo_de_trabajo(self.reloj)
            
            if proceso_terminado:
                self._registrar_estadisticas_finalizacion(proceso_terminado)
            
            if not self.kernel.planificador.cpu.esta_libre():
                self.estadisticas['uso_cpu'] += 1

            self.reloj += 1

        print(f"\n--- Simulación Finalizada en tiempo {self.reloj} ---")
        self.estadisticas['tiempo_final'] = self.reloj

    def _simulacion_finalizada(self) -> bool:
        num_terminados = len(self.kernel.gestor_colas.terminados)
        return len(self.procesos_maestros) == num_terminados

    def _registrar_estadisticas_finalizacion(self, proceso: Proceso):
        tiempo_retorno = self.reloj - proceso.tiempo_arribo
        tiempo_espera = tiempo_retorno - proceso.tiempo_irrupcion
        
        self.estadisticas['tiempos_retorno'][proceso.id] = tiempo_retorno
        self.estadisticas['tiempos_espera'][proceso.id] = tiempo_espera
        print(f"Proceso {proceso.id} terminado. Retorno: {tiempo_retorno}, Espera: {tiempo_espera}")

    def generar_reporte_estadistico(self) -> dict:
        print("\n--- Reporte Estadístico ---")
        num_terminados = len(self.estadisticas['tiempos_retorno'])
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