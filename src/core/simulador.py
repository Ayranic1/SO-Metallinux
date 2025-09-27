#  Definición básica para arrancar, después lo cambiamos

from .cpu import CPU
from .gestor_memoriaBestFit import GestorMemoriaBestFit
from .planificadorSRTF import PlanificadorSRTF
from .colas import GestorColas

class Simulador:
    def __init__(self):
        self.reloj = 0  # Para simular el paso de tiempo
        self.cpu = CPU()
        self.gestor_memoria = GestorMemoriaBestFit()
        
        # Crear el gestor de colas primero 
        self.gestor_colas = GestorColas()
        
        # Crear el planificador pasando el gestor de colas
        self.planificador = PlanificadorSRTF(self.gestor_colas)
