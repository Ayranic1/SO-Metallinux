from abc import ABC, abstractmethod
from .plantillas import GestorMemoria
from .particion import Particion


class GestorMemoriaBestFit(GestorMemoria):
    
    
    def encontrar_particion(self, tamaño_proceso: int):
        # se busca la partició acorde a la política de asignación best-fit

        espacio_ideal = 550
        for particion in self.particiones:
            if particion.esta_libre():
                espacio_libre = particion.tamaño - tamaño_proceso
                if ((espacio_libre > 0) and (espacio_libre < espacio_ideal)):
                    particion_ideal = particion
                    espacio_ideal = espacio_libre
        
        if (espacio_ideal!=550):
            return particion_ideal.id
        else: return False



#  100K destinados al Sistema Operativo. v
#  250K para trabajos los más grandes.
#  150K para trabajos medianos .
#  50K  para trabajos pequeños.