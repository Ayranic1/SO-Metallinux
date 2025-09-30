# Clase base para arrancar, si necesitas agregar mas cosas hacelo

class Particion:
    def __init__(self, id: str, direccion_inicio: int, tamaño: int):
        self.id = id
        self.direccion_inicio = direccion_inicio
        self.tamaño = tamaño
        self.proceso_asignado = None
        self.fragmentacion_interna = 0
    
    def __str__(self):
        return f"Partición {self.id}: {self.tamaño}K, inicio: {self.direccion_inicio}"
    
    # TO DO: Implementar método para asignar proceso a esta partición
    def asignar_proceso(self, proceso):
        pass
    
    # TO DO: Implementar método para liberar la partición
    def liberar(self):
        pass
    
    # TODO: Implementar método para verificar si está libre
    def esta_libre(self):
        pass
    
    # TO DO: Implementar método para obtener espacio disponible
    def espacio_disponible(self):
        pass


# 100K destinados al Sistema Operativo
#  250K para trabajos los más grandes.
#  150K para trabajos medianos .
#  50K   para trabajos pequeños.