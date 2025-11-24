from abc import ABC, abstractmethod
from .plantillas import GestorMemoria
from .particion import Particion
from typing import Optional # Se añade para mejor tipado

class GestorMemoriaBestFit(GestorMemoria):
    
    
    def encontrar_particion(self, tamaño_proceso: int) -> Optional[str]:
        # Se busca la partición acorde a la política de asignación best-fit
        
        # Inicializar con un valor muy alto para el espacio ideal (mínima fragmentación)
        espacio_ideal = float('inf') 
        particion_ideal: Optional[Particion] = None

        for particion in self.particiones:
            # La partición '0' es para el SO y no debe usarse [cite: 58]
            if particion.esta_libre() and particion.id != '0':
                espacio_libre = particion.tamaño - tamaño_proceso
                
                # Debe caber (espacio_libre >= 0) y ser el 'mejor ajuste' (mínima fragmentación)
                if espacio_libre >= 0 and espacio_libre < espacio_ideal:
                    particion_ideal = particion
                    espacio_ideal = espacio_libre
        
        if particion_ideal:
            return particion_ideal.id
        else: 
            # Retorna False para indicar que no se encontró partición.
            return False 

#  100K destinados al Sistema Operativo. 
#  250K para trabajos los más grandes.
#  150K para trabajos medianos .
#  50K  para trabajos pequeños.