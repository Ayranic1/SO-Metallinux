import csv
import os
import sys
from typing import List, Dict, Tuple
from pathlib import Path

raiz_proyecto = Path(__file__).parent.parent.parent
sys.path.append(str(raiz_proyecto))

from src.core.proceso import Proceso

class LectorArchivos: 
    MAX_PROCESOS = 10
    
    @staticmethod
    def leer_procesos_desde_csv(ruta_archivo: str) -> Tuple[List[Proceso], List[str]]:
        # Lee un archivo CSV de procesos y devuelve lista de objetos Proceso
 
        procesos = []
        errores = []
        
        try:
            # Verificar que el archivo existe
            if not os.path.exists(ruta_archivo):
                errores.append(f"Error: El archivo '{ruta_archivo}' no existe")
                return procesos, errores
            
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector_csv = csv.DictReader(archivo)
                
                # Verificar que el archivo tiene todas las columnas necesarias
                columnas_requeridas = ['id', 'tamaño', 'tiempo_arribo', 'tiempo_irrupcion']
                if not all(col in lector_csv.fieldnames for col in columnas_requeridas):
                    errores.append("Error: El archivo CSV no tiene las columnas requeridas")
                    return procesos, errores
                
                # Leer cada fila del CSV
                for numero_fila, fila in enumerate(lector_csv, start=2):  # start=2 por el header
                    try:
                        # Validar y convertir datos
                        proceso = LectorArchivos._validar_y_crear_proceso(fila, numero_fila)
                        if proceso:
                            procesos.append(proceso)
                        else:
                            errores.append(f"Fila {numero_fila}: Datos inválidos")
                            
                    except Exception as e:
                        errores.append(f"Fila {numero_fila}: Error procesando - {str(e)}")
                
                # Validar límite de procesos
                if len(procesos) > LectorArchivos.MAX_PROCESOS:
                    errores.append(f"Error: Se excede el máximo de {LectorArchivos.MAX_PROCESOS} procesos")
                    procesos = procesos[:LectorArchivos.MAX_PROCESOS]  # Tomar solo los primeros 10
                
        except Exception as e:
            errores.append(f"Error leyendo archivo: {str(e)}")
        
        return procesos, errores
    
    @staticmethod
    def _validar_y_crear_proceso(fila: Dict, numero_fila: int) -> Proceso:
        # Valida los datos cada proceso y luego crea un objeto Proceso

        try:
            # ID
            id_proceso = fila['id'].strip()
            if not id_proceso:
                raise ValueError("ID no puede estar vacío")
            
            # Tamaño
            try:
                tamaño = int(fila['tamaño'])
                if tamaño <= 0:
                    raise ValueError("Tamaño debe ser mayor a 0")
                if tamaño > 250:  
                    raise ValueError("Tamaño excede la partición máxima (250K)")
            except ValueError:
                raise ValueError("Tamaño debe ser un número entero válido")
            
            # Tiempo de arribo
            try:
                tiempo_arribo = int(fila['tiempo_arribo'])
                if tiempo_arribo < 0:
                    raise ValueError("Tiempo de arribo no puede ser negativo")
            except ValueError:
                raise ValueError("Tiempo de arribo debe ser un número entero válido")
            
            # Tiempo de irrupción
            try:
                tiempo_irrupcion = int(fila['tiempo_irrupcion'])
                if tiempo_irrupcion <= 0:
                    raise ValueError("Tiempo de irrupción debe ser mayor a 0")
            except ValueError:
                raise ValueError("Tiempo de irrupción debe ser un número entero válido")
            
            # Crear y retornar el objeto Proceso
            return Proceso(
                id=id_proceso,
                tamaño=tamaño,
                tiempo_arribo=tiempo_arribo,
                tiempo_irrupcion=tiempo_irrupcion
            )
            
        except ValueError as e:
            raise ValueError(f"Proceso {fila.get('id', 'N/A')}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")
    
    @staticmethod
    def mostrar_errores(errores: List[str]) -> None:
        if errores:
            print("Errores encontrados en el archivo: ")
            for error in errores:
                print(f"   • {error}")
        else:
            print("Archivo leído correctamente sin errores")

    # Esto está para debug, capaz se saca pero ns
    
    @staticmethod
    def mostrar_procesos_cargados(procesos: List[Proceso]) -> None:
        print(f"Procesos cargados: {len(procesos)}")
        print("┌──────┬────────┬──────────────┬─────────────────┐")
        print("│  ID  │ Tamaño │ Tiempo Arribo│ Tiempo Irrupción│")
        print("├──────┼────────┼──────────────┼─────────────────┤")
        
        for proceso in procesos:
            print(f"│ {proceso.id:4} │ {proceso.tamaño:6} │ {proceso.tiempo_arribo:12} │ {proceso.tiempo_irrupcion:15} │")
        
        print("└──────┴────────┴──────────────┴─────────────────┘")