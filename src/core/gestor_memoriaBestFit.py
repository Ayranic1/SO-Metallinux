from abc import ABC, abstractmethod
from .interfaces import GestorMemoria

class GestorMemoriaBestFit(GestorMemoria):
    
    particiones = []

    def encontrar_particion(self, tamaño_proceso):
        pass

    # método para saber si alguna de las particiones está libre
    def estan_libres(self)-> bool:
        pass