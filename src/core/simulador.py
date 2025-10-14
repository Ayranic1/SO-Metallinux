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

    def run(self, step_by_step=False):
        print("--- Iniciando Simulación ---")
        
        while not self._simulacion_finalizada():
            print(f"\n--- Ciclo {self.reloj} ---")

            proceso_terminado = self.kernel.ciclo_de_trabajo(self.reloj)
            
            if proceso_terminado:
                self._registrar_estadisticas_finalizacion(proceso_terminado)
            
            self._imprimir_estado_ciclo()

            if not self.kernel.planificador.cpu.esta_libre():
                self.estadisticas['uso_cpu'] += 1

            if step_by_step:
                input("Presione Enter para continuar...")

            self.reloj += 1

        print(f"\n--- Simulación Finalizada en tiempo {self.reloj} ---")
        self.estadisticas['tiempo_final'] = self.reloj

    def run_to_file(self, filename):
        original_stdout = sys.stdout
        with open(filename, 'w') as f:
            sys.stdout = f
            self.run()
            self.generar_reporte_estadistico()
        sys.stdout = original_stdout

    def _simulacion_finalizada(self) -> bool:
        num_terminados = len(self.kernel.gestor_colas.terminados)
        return len(self.procesos_maestros) == num_terminados

    def _registrar_estadisticas_finalizacion(self, proceso: Proceso):
        tiempo_retorno = self.reloj - proceso.tiempo_arribo
        tiempo_espera = tiempo_retorno - proceso.tiempo_irrupcion
        
        self.estadisticas['tiempos_retorno'][proceso.id] = tiempo_retorno
        self.estadisticas['tiempos_espera'][proceso.id] = tiempo_espera
        print(f"Proceso {proceso.id} terminado. Retorno: {tiempo_retorno}, Espera: {tiempo_espera}")

    def _imprimir_estado_ciclo(self):
        # Estado del procesador
        proceso_en_cpu = self.kernel.planificador.cpu.get_proceso_actual()
        if proceso_en_cpu:
            print(f"CPU: Proceso {proceso_en_cpu.id} (Restante: {proceso_en_cpu.tiempo_restante})")
        else:
            print("CPU: Ociosa")

        # Tabla de particiones de memoria
        print("\n--- Tabla de Particiones de Memoria ---")
        print("{:<12} {:<15} {:<10} {:<15} {:<20}".format('ID Partición', 'Dirección Inicio', 'Tamaño', 'ID Proceso', 'Fragmentación Int.'))
        for p in self.kernel.gestor_memoria.particiones:
            id_proceso = p.proceso_asignado.id if p.proceso_asignado else 'N/A'
            print("{:<12} {:<15} {:<10} {:<15} {:<20}".format(p.id, p.direccion_inicio, p.tamaño, id_proceso, p.fragmentacion_interna))

        # Cola de procesos listos
        print("\n--- Cola de Listos ---")
        if self.kernel.gestor_colas.listos:
            print(", ".join([p.id for p in self.kernel.gestor_colas.listos]))
        else:
            print("(Vacía)")

        # Cola de procesos suspendidos
        print("\n--- Cola de Suspendidos ---")
        if self.kernel.gestor_colas.suspendidos:
            print(", ".join([p.id for p in self.kernel.gestor_colas.suspendidos]))
        else:
            print("(Vacía)")

    def generar_reporte_estadistico(self) -> dict:
        print("\n--- Reporte Estadístico ---")
        num_terminados = len(self.estadisticas['tiempos_retorno'])

        # Tiempos de retorno y espera por proceso
        print("\n--- Tiempos por Proceso ---")
        print("{:<10} {:<15} {:<15}".format('Proceso', 'T. Retorno', 'T. Espera'))
        for pid in self.estadisticas['tiempos_retorno']:
            print("{:<10} {:<15} {:<15}".format(pid, self.estadisticas['tiempos_retorno'][pid], self.estadisticas['tiempos_espera'][pid]))

        if num_terminados == 0:
            reporte = {
                "Tiempo promedio de retorno": 0,
                "Tiempo promedio de espera": 0,
                "Uso de CPU (%)": 0,
                "Rendimiento": 0
            }
        else:
            total_retorno = sum(self.estadisticas['tiempos_retorno'].values())
            total_espera = sum(self.estadisticas['tiempos_espera'].values())
            tiempo_final = self.estadisticas['tiempo_final']
            uso_cpu_porcentaje = (self.estadisticas['uso_cpu'] / tiempo_final) * 100 if tiempo_final > 0 else 0
            rendimiento = num_terminados / tiempo_final if tiempo_final > 0 else 0
            
            reporte = {
                "Tiempo promedio de retorno": total_retorno / num_terminados,
                "Tiempo promedio de espera": total_espera / num_terminados,
                "Uso de CPU (%)": uso_cpu_porcentaje,
                "Rendimiento": rendimiento
            }
        
        print("\n--- Métricas Generales ---")
        for key, value in reporte.items():
            print(f"{key}: {value:.2f}")
        return reporte
