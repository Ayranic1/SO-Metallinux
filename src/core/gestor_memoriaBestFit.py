from abc import ABC, abstractmethod
from .plantillas import GestorMemoria
from .particion import Particion
from typing import Optional # Se añade para mejor tipado

class GestorMemoriaBestFit(GestorMemoria):
    """
    Implementa el algoritmo de gestión de memoria Best-Fit.
    Busca la partición libre que mejor se ajuste al tamaño del proceso para minimizar
    la fragmentación interna.
    """
    def encontrar_particion(self, tamaño_proceso: int) -> Optional[str]:
        """
        Encuentra la partición libre que deja el menor espacio remanente (fragmentación).
        """
        espacio_ideal = float('inf') 
        particion_ideal: Optional[Particion] = None

        for particion in self.particiones:
            # La partición '0' está reservada para el SO.
            if particion.esta_libre() and particion.id != '0':
                espacio_libre = particion.tamaño - tamaño_proceso
                
                # La partición debe ser lo suficientemente grande y la que minimice el desperdicio.
                if espacio_libre >= 0 and espacio_libre < espacio_ideal:
                    particion_ideal = particion
                    espacio_ideal = espacio_libre
        
        if particion_ideal:
            return particion_ideal.id
        else: 
            return False