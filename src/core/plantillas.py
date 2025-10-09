from abc import ABC, abstractmethod
from typing import Optional
from .proceso import Proceso
from .colas import GestorColas
from .cpu import CPU

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
        pass
    
    # TO DO: Implementar algoritmo (en este caso BEST-FIT) para asignación de memoria
    # Es solo el algoritmo puro
    @abstractmethod
    def encontrar_particion(self, tamaño_proceso):
        pass
    
    # TO DO: Implementar método para asignar proceso a memoria
    # Utiliza encontrar_particion para tomar la decision y aplica los cambios en memoria
    def asignar_memoria(self, proceso):
        pass
    
    # TO DO: Implementar método para liberar memoria de un proceso
    def liberar_memoria(self, proceso):
        pass
    
    # TO DO: Implementar método para obtener estado de memoria
    def obtener_estado_memoria(self):
        pass
    
    # TO DO: Implementar método para verificar grado de multiprogramación
    def grado_multiprogramacion_actual(self):
        pass

class Planificador(ABC):
    def __init__(self, gestor_colas: GestorColas, cpu: CPU):
        self.gestor_colas = gestor_colas
        self.cpu = cpu 
        self.tiempo_actual = 0

    @abstractmethod
    def seleccionar_proximo_proceso_listo(self) -> Optional[Proceso]:
        pass

    def ejecutar(self) -> Optional[Proceso]:
        if self._necesita_preempcion():
            self._preemptar()
        
        if self.cpu.esta_libre():
            proximo = self.seleccionar_proximo_proceso_listo()
            if proximo:
                self._asignar_cpu(proximo)
        
        return self.cpu.get_proceso_actual()

    def manejar_llegadas(self, procesos_nuevos: list):
        for proceso in procesos_nuevos:
            if proceso.tiempo_arribo == self.tiempo_actual:
                print(f"Tiempo {self.tiempo_actual}: Llega el proceso {proceso.id}")
                self.gestor_colas.agregar_nuevo(proceso)

    def manejar_finalizacion(self) -> Optional[Proceso]:
        proceso_en_cpu = self.cpu.get_proceso_actual()
        if proceso_en_cpu and proceso_en_cpu.tiempo_restante <= 0:
            proceso_terminado = self.cpu.liberar() 
            proceso_terminado.estado = "Terminado"
            print(f"Tiempo {self.tiempo_actual}: Finaliza el proceso {proceso_terminado.id}")
            self.gestor_colas.terminados.append(proceso_terminado) 
            return proceso_terminado
        return None

    def avanzar_tiempo(self):
        self.tiempo_actual += 1
        self.cpu.ejecutar_ciclo()

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
        self.cpu.dispatch(proceso)
        print(f"Tiempo {self.tiempo_actual}: Se asigna CPU al proceso {proceso.id}")