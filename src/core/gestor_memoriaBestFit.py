from abc import ABC, abstractmethod
from .interfaces import GestorMemoria
from particion import Particion


class GestorMemoriaBestFit(GestorMemoria):
    
    particiones = []

    # realiza las particiones 
    def realizar_particiones(self):
        tams = [100, 250, 150, 50] # tamaños de particiones
        id=0
        ult_dir = 0
        for t in tams:
            self.particiones[id] = Particion(str(id),ult_dir, t)
            ult_dir+= t
            id+=1

    
    def encontrar_particion(self, tamaño_proceso):
        # se busca la partició acorde a la política de asignación best-fit

        espacio_ideal = 550
        for particion in self.particiones:

            if particion.esta_libre():
                espacio_libre = particion.tamaño - tamaño_proceso
                if ((espacio_libre > 0) and (espacio_libre < espacio_ideal)):
                    particion_ideal = particion
                    espacio_ideal = espacio_libre
        
        if (espacio_ideal!=550):
            return particion_ideal
        else: return False

    # método para saber si alguna de las particiones está libre
    def hay_libre(self)-> bool:
        for particion in self.particiones:
            if particion.disponible():
                return True
        return False


#  100K destinados al Sistema Operativo.
#  250K para trabajos los más grandes.
#  150K para trabajos medianos .
#  50K  para trabajos pequeños.