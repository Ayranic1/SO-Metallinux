import os
import sys

sys.path.append(os.path.dirname(__file__))

from utils.archivo_reader import LectorArchivos

def main():
    ruta_archivo = "data/procesos.csv"
    
    print("Leyendo archivo de procesos...")
    procesos, errores = LectorArchivos.leer_procesos_desde_csv(ruta_archivo)
    
    LectorArchivos.mostrar_errores(errores)
    LectorArchivos.mostrar_procesos_cargados(procesos)
    
    if procesos:
        print("Iniciando simulación...")
        # TO DO : llamar los metodos para el simulador
    else:
        print("No se pueden cargar procesos debido a errores")

if __name__ == "__main__":
    main()