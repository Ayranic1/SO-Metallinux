# Clase base para arrancar, si necesitas agregar mas cosas hacelo
from typing import TYPE_CHECKING
from .proceso import Proceso

if TYPE_CHECKING:
    from .colas import GestorColas

class Particion:
    def __init__(self, id: str, direccion_inicio: int, tamaño: int):
        self.id = id
        self.direccion_inicio = direccion_inicio
        self.tamaño = tamaño
        self.proceso_asignado = None
        self.fragmentacion_interna = 0
        
    
    def __str__(self):
        return f"Partición {self.id}: {self.tamaño}K, inicio: {self.direccion_inicio}"

    def liberar(self, gestorColas : 'GestorColas'):
        # Método para liberar la partición del proceso asignado y lo pone en la cola de terminados
        gestorColas.terminados.append(self.proceso_asignado)
        self.proceso_asignado = None
    
    def espacio_disponible(self):
        # devuelve el espacio de la partición
        return self.tamaño - self.proceso_asignado.tamaño()

        
    def esta_libre(self)->bool:
        return self.proceso_asignado is None



#  100K destinados al Sistema Operativo.
#  250K para trabajos los más grandes.
#  150K para trabajos medianos .
#  50K  para trabajos pequeños.