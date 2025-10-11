from abc import ABC, abstractmethod
from .interfaces import GestorMemoria
from particion import Particion


class GestorMemoriaBestFit(GestorMemoria):
    

    # realiza las particiones 
    def realizar_particiones(self, cola_listo: list)->list:
        tams = [100, 250, 150, 50] # tamaños de particiones
        id=0
        ult_dir = 0
        for t in tams:
            cola_listo[id] = Particion(str(id),ult_dir, t)
            ult_dir+= t
            id+=1

        return cola_listo

    
    def encontrar_particion(self, tamaño_proceso: int, cola_listo: list):
        # se busca la partició acorde a la política de asignación best-fit

        espacio_ideal = 550
        for particion in cola_listo:

            if particion.esta_libre():
                espacio_libre = particion.tamaño - tamaño_proceso
                if ((espacio_libre > 0) and (espacio_libre < espacio_ideal)):
                    particion_ideal = particion
                    espacio_ideal = espacio_libre
        
        if (espacio_ideal!=550):
            return particion_ideal.id
        else: return False

    # método para saber si alguna de las particiones está libre
    def hay_libre(self, cola_listo: list)-> bool:
        for particion in cola_listo:
            if particion.esta_libre():
                return True
        return False

    # método para agregar un proceso a memoria
    def proceso_a_memoria(self, cola_listo: list, cola_del_proceso: list)->bool :
        
        if self.hay_libre(cola_listo):
            proceso = cola_del_proceso[0]
            id = self.encontrar_particion(proceso.tamaño, cola_listo)
            if id != False:
                cola_listo[id] = proceso
                cola_del_proceso.pop(0)
                return True

        return False

#  100K destinados al Sistema Operativo.
#  250K para trabajos los más grandes.
#  150K para trabajos medianos .
#  50K  para trabajos pequeños.