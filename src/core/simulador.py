import sys
import os
from typing import List
from .proceso import Proceso
from .cpu import CPU
from .colas import GestorColas
from .gestor_memoriaBestFit import GestorMemoriaBestFit
from .planificadorSRTF import PlanificadorSRTF
from .kernel import Kernel

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    print("Tabulate library not found. Por favor, instale tabulate: pip install tabulate")
    tabulate = None
    TABULATE_AVAILABLE = False

class Simulador:
    """
    Orquesta la simulación completa, gestionando el reloj, los componentes del sistema
    y la recolección de estadísticas.
    """
    def __init__(self, procesos: List[Proceso], verbose: bool = True):
        self.reloj = 0
        self.procesos_maestros = procesos
        self.verbose = verbose
        self.total_procesos_cargados = len(procesos)

        # Componentes del sistema
        cpu = CPU()
        gestor_colas = GestorColas()
        gestor_memoria = GestorMemoriaBestFit()
        planificador = PlanificadorSRTF(gestor_colas, cpu)
        
        # El kernel centraliza la lógica de control del sistema
        self.kernel = Kernel(
            self.procesos_maestros,
            gestor_memoria,
            planificador,
            gestor_colas,
            self.verbose
        )
        
        # Diccionario para almacenar las métricas de la simulación
        self.estadisticas = {
            'tiempos_arribo': {},
            'tiempos_finalizacion': {},
            'tiempos_retorno': {},
            'tiempos_espera': {},
            'uso_cpu': 0,
            'tiempo_final': 0,
        }

    def _get_current_simulation_state(self):
        # Captura el estado para detectar cambios estructurales en el sistema
        return {
            'cpu_id': self.kernel.planificador.cpu.get_proceso_actual().id if self.kernel.planificador.cpu.get_proceso_actual() else None,
            'listos': tuple(sorted([p.id for p in self.kernel.gestor_colas.listos])),
            'suspendidos': tuple(sorted([p.id for p in self.kernel.gestor_colas.suspendidos])),
            'nuevos': tuple(sorted([p.id for p in self.kernel.gestor_colas.nuevos])),
            'particiones': tuple(
                (p.id, p.proceso_asignado.id if p.proceso_asignado else None) 
                for p in self.kernel.gestor_memoria.particiones
            )
        }

    def run(self, step_by_step=False):
        """
        Ejecuta el bucle principal de la simulación hasta que todos los procesos hayan terminado.
        """
        if self.verbose:
            print("--- Iniciando Simulación ---")
        
        while not self._simulacion_finalizada():
            proceso_terminado, eventos = self.kernel.ciclo_de_trabajo(self.reloj)
            
            if proceso_terminado:
                self._registrar_estadisticas_finalizacion(proceso_terminado)

            is_significant_event = bool(eventos) or self.reloj == 0

            if is_significant_event:
                if step_by_step:
                    if self.verbose:
                        os.system('cls' if os.name == 'nt' else 'clear')
                    self._imprimir_estado_ciclo(eventos)
                    input("Presione Enter para continuar...")
                else:
                    self._imprimir_estado_ciclo(eventos)
            
            if not self.kernel.planificador.cpu.esta_libre():
                self.estadisticas['uso_cpu'] += 1

            self.reloj += 1

        if self.verbose:
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
        # La simulación termina cuando todos los procesos iniciales han sido completados.
        num_terminados = len(self.kernel.gestor_colas.terminados)
        return self.total_procesos_cargados == num_terminados

    def _registrar_estadisticas_finalizacion(self, proceso: Proceso):
        tiempo_retorno = self.reloj - proceso.tiempo_arribo
        tiempo_espera = tiempo_retorno - proceso.tiempo_irrupcion
        
        self.estadisticas['tiempos_arribo'][proceso.id] = proceso.tiempo_arribo
        self.estadisticas['tiempos_finalizacion'][proceso.id] = self.reloj
        self.estadisticas['tiempos_retorno'][proceso.id] = tiempo_retorno
        self.estadisticas['tiempos_espera'][proceso.id] = tiempo_espera
        if self.verbose:
            print(f"Proceso {proceso.id} terminado. Retorno: {tiempo_retorno}, Espera: {tiempo_espera}")

    def _imprimir_estado_ciclo(self, eventos: List[str]):
        print(f"\n--- Ciclo {self.reloj} ---")
        
        # Imprime los eventos ocurridos en el ciclo
        for evento in eventos:
            print(evento)
            
        proceso_en_cpu = self.kernel.planificador.cpu.get_proceso_actual()
        
        # Muestra el grado de multiprogramación actual
        current_dom = self.kernel._get_current_dom()

        # Muestra el estado de las particiones de memoria
        print("\n--- Tabla de Particiones de Memoria ---")
        headers = ['ID Partición', 'Dirección Inicio', 'Tamaño', 'ID Proceso', 'Fragmentación Int.']
        table = []
        for p in self.kernel.gestor_memoria.particiones:
            id_proceso = p.proceso_asignado.id if p.proceso_asignado else 'Libre'
            frag_interna = p.fragmentacion_interna if p.fragmentacion_interna is not None else 0
            table.append([p.id, p.direccion_inicio, p.tamaño, id_proceso, frag_interna])
        
        if TABULATE_AVAILABLE:
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(self._crear_tabla_manual(headers, table))

        # Muestra el estado de las colas de procesos
        print("\n--- Cola de Listos (Asignados / Orden SRTF) ---")
        if self.kernel.gestor_colas.listos:
            headers_listos = ['ID', 'T. Restante', 'T. Irrupción', 'Tamaño']
            table_listos = [[p.id, p.tiempo_restante, p.tiempo_irrupcion, p.tamaño] for p in self.kernel.gestor_colas.listos]
            if TABULATE_AVAILABLE:
                print(tabulate(table_listos, headers=headers_listos, tablefmt="grid"))
            else:
                print(self._crear_tabla_manual(headers_listos, table_listos))
        else:
            print("(Vacía)")

        print("\n--- Cola de Listos y Suspendidos (Admitidos / Sin Memoria) ---")
        if self.kernel.gestor_colas.suspendidos:
            headers_suspendidos = ['ID', 'T. Arribo', 'T. Irrupción', 'Tamaño', 'T. Restante']
            table_suspendidos = [[p.id, p.tiempo_arribo, p.tiempo_irrupcion, p.tamaño, p.tiempo_restante] for p in self.kernel.gestor_colas.suspendidos]
            if TABULATE_AVAILABLE:
                print(tabulate(table_suspendidos, headers=headers_suspendidos, tablefmt="grid"))
            else:
                print(self._crear_tabla_manual(headers_suspendidos, table_suspendidos))
        else:
            print("(Vacía)")
            
        print("\n--- Cola de Nuevos (Esperando Admisión al DOM) ---")
        if self.kernel.gestor_colas.nuevos:
            headers_nuevos = ['ID', 'T. Arribo', 'T. Irrupción', 'Tamaño']
            table_nuevos = [[p.id, p.tiempo_arribo, p.tiempo_irrupcion, p.tamaño] for p in self.kernel.gestor_colas.nuevos]
            if TABULATE_AVAILABLE:
                print(tabulate(table_nuevos, headers=headers_nuevos, tablefmt="grid"))
            else:
                print(self._crear_tabla_manual(headers_nuevos, table_nuevos))
        else:
            print("(Vacía)")

    def _crear_tabla_manual(self, headers, data):
        """Crea una tabla ASCII manualmente cuando tabulate no está disponible"""
        col_widths = [len(str(h)) for h in headers]
        for row in data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
        separator = "-+-".join("-" * w for w in col_widths)
        
        lines = [header_line, separator]
        for row in data:
            lines.append(" | ".join(f"{str(c):<{col_widths[i]}}" for i, c in enumerate(row)))
        return "\n".join(lines)

    def generar_reporte_estadistico(self) -> dict:
        """
        Calcula y muestra las métricas finales de la simulación.
        """
        print("\n" + "="*50)
        print("REPORTE ESTADÍSTICO FINAL")
        print("="*50)

        num_terminados = len(self.estadisticas['tiempos_retorno'])

        # Muestra una tabla con los tiempos consolidados por proceso
        print("\n--- TIEMPOS POR PROCESO ---")
        headers = ['Proceso', 'T. Arribo', 'T. Finalización', 'T. Retorno', 'T. Espera']
        table = []
        for pid in sorted(self.estadisticas['tiempos_retorno'].keys()):
            table.append([
                pid,
                self.estadisticas['tiempos_arribo'][pid],
                self.estadisticas['tiempos_finalizacion'][pid],
                self.estadisticas['tiempos_retorno'][pid],
                self.estadisticas['tiempos_espera'][pid]
            ])
        
        if TABULATE_AVAILABLE:
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(self._crear_tabla_manual(headers, table))

        # Muestra las métricas generales del sistema
        if num_terminados == 0:
            reporte = {
                "Tiempo promedio de retorno (u.t)": 0,
                "Tiempo promedio de espera (u.t)": 0,
                "Rendimiento (procesos/u.t)": 0,
                "Tiempo de simulación total (u.t)": self.estadisticas['tiempo_final']
            }
        else:
            total_retorno = sum(self.estadisticas['tiempos_retorno'].values())
            total_espera = sum(self.estadisticas['tiempos_espera'].values())
            tiempo_final = self.estadisticas['tiempo_final']
            rendimiento = num_terminados / tiempo_final if tiempo_final > 0 else 0
            
            reporte = {
                "Tiempo promedio de retorno (u.t)": total_retorno / num_terminados,
                "Tiempo promedio de espera (u.t)": total_espera / num_terminados,
                "Rendimiento (procesos/u.t)": rendimiento,
                "Tiempo de simulación total (u.t)": tiempo_final
            }
        
        print("\n--- MÉTRICAS GENERALES ---")
        headers = ["Métrica", "Valor"]
        table = []
        for key, value in reporte.items():
            if key == "Tiempo de simulación total (u.t)":
                 table.append([key, f"{value}"])
            else:
                table.append([key, f"{value:.2f}"])
        
        if TABULATE_AVAILABLE:
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(self._crear_tabla_manual(headers, table))

        return reporte