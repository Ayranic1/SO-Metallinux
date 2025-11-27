import os
import sys

sys.path.append(os.path.dirname(__file__))

from utils.archivo_reader import LectorArchivos
from core.simulador import Simulador

def seleccionar_archivo_csv():
    # Muestra los archivos CSV disponibles en la carpeta data/ y pide al usuario que seleccione uno
    # Determinar la ruta absoluta de la carpeta data/ 
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
    
    # Listar solo archivos .csv en el directorio de datos
    try:
        archivos_csv = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    except FileNotFoundError:
        print(f"\nError: El directorio 'data' no se encontró en {data_dir}.")
        return None, None
    
    if not archivos_csv:
        print("\nError: No se encontraron archivos .csv en la carpeta 'data'.")
        return None, None
    
    print("\n--- Archivos CSV disponibles en data/ ---")
    for i, filename in enumerate(archivos_csv):
        print(f"[{i + 1}]. {filename}")
        
    while True:
        try:
            opcion = input("Seleccione el número del archivo a cargar: ")
            indice = int(opcion) - 1
            if 0 <= indice < len(archivos_csv):
                nombre_archivo = archivos_csv[indice]
                ruta_completa = os.path.join(data_dir, nombre_archivo)
                return ruta_completa, nombre_archivo
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

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
    print("[2]. Ejecutar simulación solo cambios")
    print("[3]. Ejecutar simulación completa")
    print("[4]. Guardar informe en archivo")
    print("[5]. Salir")

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
            print("Iniciando simulación ...")
            simulador = Simulador(procesos)
            simulador.run(solo_cambios=True)
            simulador.generar_reporte_estadistico()
            break
        elif opcion == '3':
            print("Iniciando simulación completa...")
            simulador = Simulador(procesos)
            simulador.run()
            simulador.generar_reporte_estadistico()
            break
        elif opcion == '4':
            print("Iniciando simulación y guardando informe en archivo...")
            simulador = Simulador(procesos)
            simulador.run_to_file("informe_simulacion.txt")
            print("Informe guardado en 'informe_simulacion.txt'")
            break
        elif opcion == '5':
            print("Saliendo del simulador.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
