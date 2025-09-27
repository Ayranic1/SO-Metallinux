from abc import ABC, abstractmethod
from .interfaces import GestorMemoria

class GestorMemoriaBestFit(GestorMemoria):
    def encontrar_particion(self, tamaño_proceso):
        pass