# Clase base para arrancar, si necesitas agregar mas cosas hacelo

class GestorMemoria:
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
    
    # TO DO: Implementar algoritmo BEST-FIT para asignación de memoria
    def best_fit(self, tamaño_proceso):
        pass
    
    # TO DO: Implementar método para asignar proceso a memoria
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