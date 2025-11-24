import sys
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
        proceso_en_cpu = self.kernel.planificador.cpu.get_proceso_actual()
        cpu_status = f"Proceso {proceso_en_cpu.id} (Restante: {proceso_en_cpu.tiempo_restante})" if proceso_en_cpu else "Ociosa"
        print(f"CPU: {cpu_status}")

        # Tabla de Particiones de Memoria
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
            # Formato manual mejorado para tablas ASCII
            print(self._crear_tabla_manual(headers, table))

        # --- Colas de Procesos Detalladas ---

        # 1. Cola de procesos listos
        print("\n--- Cola de Listos ---")
        if self.kernel.gestor_colas.listos:
            headers_listos = ['ID', 'T. Restante', 'T. Irrupción', 'Tamaño']
            table_listos = [[p.id, p.tiempo_restante, p.tiempo_irrupcion, p.tamaño] for p in self.kernel.gestor_colas.listos]
            if TABULATE_AVAILABLE:
                print(tabulate(table_listos, headers=headers_listos, tablefmt="grid"))
            else:
                print(self._crear_tabla_manual(headers_listos, table_listos))
        else:
            print("(Vacía)")

        # 2. Cola de Listos y Suspendidos
        print("\n--- Cola de Listos y Suspendidos ---")
        if self.kernel.gestor_colas.suspendidos:
            headers_suspendidos = ['ID', 'T. Arribo', 'T. Irrupción', 'Tamaño', 'T. Restante']
            table_suspendidos = [[p.id, p.tiempo_arribo, p.tiempo_irrupcion, p.tamaño, p.tiempo_restante] for p in self.kernel.gestor_colas.suspendidos]
            if TABULATE_AVAILABLE:
                print(tabulate(table_suspendidos, headers=headers_suspendidos, tablefmt="grid"))
            else:
                print(self._crear_tabla_manual(headers_suspendidos, table_suspendidos))
        else:
            print("(Vacía)")
            
        # 3. Cola de procesos nuevos
        print("\n--- Cola de Nuevos ---")
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
        # Calcular anchos de columnas
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(str(header))
            for row in data:
                max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width + 2)  # +2 para padding
        
        # Crear línea separadora
        separator = "┌"
        for width in col_widths:
            separator += "─" * width + "┬"
        separator = separator[:-1] + "┐"
        
        # Crear línea de headers
        header_line = "│"
        for i, header in enumerate(headers):
            header_line += f" {header:<{col_widths[i]-2}} │"
        
        # Crear línea media
        middle_sep = "├"
        for width in col_widths:
            middle_sep += "─" * width + "┼"
        middle_sep = middle_sep[:-1] + "┤"
        
        # Crear líneas de datos
        data_lines = []
        for row in data:
            data_line = "│"
            for i, cell in enumerate(row):
                data_line += f" {str(cell):<{col_widths[i]-2}} │"
            data_lines.append(data_line)
        
        # Crear línea final
        bottom_sep = "└"
        for width in col_widths:
            bottom_sep += "─" * width + "┴"
        bottom_sep = bottom_sep[:-1] + "┘"
        
        # Construir tabla completa
        table_str = separator + "\n" + header_line + "\n" + middle_sep + "\n"
        table_str += "\n".join(data_lines) + "\n" + bottom_sep
        
        return table_str

    def generar_reporte_estadistico(self) -> dict:
        print("\n" + "="*50)
        print("REPORTE ESTADÍSTICO FINAL")
        print("="*50)

        num_terminados = len(self.estadisticas['tiempos_retorno'])

        # Tabla de tiempos por proceso
        print("\n--- TIEMPOS POR PROCESO ---")
        headers = ['Proceso', 'T. Retorno', 'T. Espera']
        table = []
        for pid in self.estadisticas['tiempos_retorno']:
            table.append([pid, self.estadisticas['tiempos_retorno'][pid], self.estadisticas['tiempos_espera'][pid]])
        
        if TABULATE_AVAILABLE:
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(self._crear_tabla_manual(headers, table))

        # Métricas generales
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
        
        print("\n--- MÉTRICAS GENERALES ---")
        headers = ["Métrica", "Valor"]
        table = []
        for key, value in reporte.items():
            table.append([key, f"{value:.2f}"])
        
        if TABULATE_AVAILABLE:
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print(self._crear_tabla_manual(headers, table))

        return reporte