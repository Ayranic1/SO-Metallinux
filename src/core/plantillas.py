from abc import ABC, abstractmethod
from typing import Optional
from .proceso import Proceso
from .colas import GestorColas
from particion import Particion

# Clase base para arrancar, si necesitas agregar mas cosas hacelo

class GestorMemoria(ABC):
    def __init__(self):
        self.particiones = []
        # TO DO: Inicializar las particiones fijas según especificación:
        # - 100K para Sistema Operativo (no disponible para procesos)
        # - 250K para trabajos grandes
        # - 150K para trabajos medianos  
        # - 50K para trabajos pequeños
        # - Calcular direcciones de inicio apropiadas
        self.inicializar_particiones()
    
    def inicializar_particiones(self):
        # TO DO: Crear e inicializar la lista de particiones
        tams = [100, 250, 150, 50] # tamaños de particiones
        id=0
        ult_dir = 0
        for t in tams:
            particion = Particion(str(id),ult_dir, t)
            self.particiones.append(particion)
            ult_dir+= t
            id+=1

    # TO DO: Implementar algoritmo (en este caso BEST-FIT) para asignación de memoria
    # Es solo el algoritmo puro 
    @abstractmethod
    def encontrar_particion(self, tamaño_proceso):
        pass
    
    # TO DO: Implementar método para asignar proceso a memoria
    # Utiliza encontrar_particion para tomar la decision y aplica los cambios en memoria
    def asignar_memoria(self, proceso):

        if self.hay_libre(self.particiones):
            id = self.encontrar_particion(proceso.tamaño, self.particiones)
            if id != False:
                self.particiones[id] = proceso
                # return True

        # return False
    
    # TO DO: Implementar método para liberar memoria de un proceso
    def liberar_memoria(self, proceso):
        for particion in self.particiones:
            if (particion.proceso_asignado == proceso):
                particion.proceso_asignado = None
        
    
    # TO DO: Implementar método para obtener estado de memoria
    def mostrar_estado_memoria(self):
        """
            Devuelve un diccionario con los estados de cada partición
        """
        estado_actual = []
    
        for particion in self.particiones:
        
            if particion.proceso_asignado is None:
                estado = "Libre"
                proceso_info = "N/A"
            else:
                estado = "Ocupada"

                proceso_info = f"PID={particion.proceso_asignado.pid}, Nombre='{particion.proceso_asignado.nombre}'"
            
            registro = {
                "ID_Particion": particion.id_particion,
                "Tamaño": particion.tamano,
                "Estado": estado,
                "Proceso_Asignado": proceso_info
            }
            estado_actual.append(registro)
            
        return estado_actual
    
    # TO DO: Implementar método para verificar grado de multiprogramación
    def grado_multiprogramacion_actual(self):
        grado = 0
        for particion in self.particiones:
            if particion.proceso_asignado != None:
                grado += 1
        return grado
    
    # método para saber si alguna de las particiones está libre
    def hay_libre(self)-> bool:
        for particion in self.particiones:
            if particion.esta_libre():
                return True
        return False



class Planificador(ABC):
    def __init__(self, gestor_colas: GestorColas):
        self.gestor_colas = gestor_colas
        self.tiempo_actual = 0

    @abstractmethod
    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        pass

    def ejecutar(self) -> Optional[Proceso]:
        # La finalización ahora se maneja en el bucle principal del simulador
        if self.gestor_colas.ejecucion and self._necesita_preempcion():
            self._preemptar()
        
        if self.gestor_colas.ejecucion is None:
            proximo = self.seleccionar_proximo_proceso_listo()
            if proximo:
                self._asignar_cpu(proximo)
        
        return self.gestor_colas.ejecucion

    def manejar_llegadas(self, procesos_nuevos: list):
        for proceso in procesos_nuevos:
            if proceso.tiempo_arribo == self.tiempo_actual:
                print(f"Tiempo {self.tiempo_actual}: Llega el proceso {proceso.id}")
                self.gestor_colas.agregar_nuevo(proceso)

    def manejar_finalizacion(self) -> Optional[Proceso]:
        if self.gestor_colas.ejecucion and self.gestor_colas.ejecucion.tiempo_restante <= 0:
            proceso_terminado = self.gestor_colas.ejecucion
            proceso_terminado.estado = "Terminado"
            print(f"Tiempo {self.tiempo_actual}: Finaliza el proceso {proceso_terminado.id}")
            self.gestor_colas.liberar_cpu(terminado=True)
            return proceso_terminado
        return None

    def avanzar_tiempo(self):
        self.tiempo_actual += 1
        if self.gestor_colas.ejecucion:
            self.gestor_colas.ejecucion.tiempo_restante -= 1

    # Métodos que deben ser implementados por el planificador concreto (SRTF)
    @abstractmethod
    def _necesita_preempcion(self) -> bool:
        pass

    @abstractmethod
    def _preemptar(self):
        pass

    # Métodos auxiliares que el planificador concreto usará
    def _asignar_cpu(self, proceso: Proceso):
        self.gestor_colas.listos.remove(proceso)
        proceso.estado = "Ejecucion"
        self.gestor_colas.ejecucion = proceso
        print(f"Tiempo {self.tiempo_actual}: Se asigna CPU al proceso {proceso.id}")