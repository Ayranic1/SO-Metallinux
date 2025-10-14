import os
import sys

sys.path.append(os.path.dirname(__file__))

from utils.archivo_reader import LectorArchivos
from core.simulador import Simulador

def mostrar_menu():
    nombre_grupo = """
                    
                ███╗░░░███╗███████╗████████╗░█████╗░██╗░░░░░██╗░░░░░██╗███╗░░██╗██╗░░░██╗██╗░░██╗
                ████╗░████║██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░░░░░██║████╗░██║██║░░░██║╚██╗██╔╝
                ██╔████╔██║█████╗░░░░░██║░░░███████║██║░░░░░██║░░░░░██║██╔██╗██║██║░░░██║░╚███╔╝░
                ██║╚██╔╝██║██╔══╝░░░░░██║░░░██╔══██║██║░░░░░██║░░░░░██║██║╚████║██║░░░██║░██╔██╗░
                ██║░╚═╝░██║███████╗░░░██║░░░██║░░██║███████╗███████╗██║██║░╚███║╚██████╔╝██╔╝╚██╗
                ╚═╝░░░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝
          
    """
    s = " "
    print(f"{s:^30}" + nombre_grupo)
    print(f"{s:^30}Bienvenido al Simulador de Sistema Operativo")
    print(f"{s:^5}Este simulador utiliza el algoritmo SRTF para la planificación de CPU y Best-Fit para la gestión de memoria.")
    print("\nOpciones:")
    print("[1]. Ejecutar simulación paso a paso")
    print("[2]. Ejecutar simulación completa")
    print("[3]. Guardar informe en archivo")
    print("[4]. Salir")

def main():
    ruta_archivo = "data/procesos.csv"
    
    print("Leyendo archivo de procesos...")
    procesos, errores = LectorArchivos.leer_procesos_desde_csv(ruta_archivo)
    
    LectorArchivos.mostrar_errores(errores)
    LectorArchivos.mostrar_procesos_cargados(procesos)
    
    if not procesos:
        print("No se pueden cargar procesos debido a errores")
        return

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("Iniciando simulación paso a paso...")
            simulador = Simulador(procesos)
            simulador.run(step_by_step=True)
            simulador.generar_reporte_estadistico()
            break
        elif opcion == '2':
            print("Iniciando simulación completa...")
            simulador = Simulador(procesos)
            simulador.run()
            simulador.generar_reporte_estadistico()
            break
        elif opcion == '3':
            print("Iniciando simulación y guardando informe en archivo...")
            simulador = Simulador(procesos)
            simulador.run_to_file("informe_simulacion.txt")
            print("Informe guardado en 'informe_simulacion.txt'")
            break
        elif opcion == '4':
            print("Saliendo del simulador.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
