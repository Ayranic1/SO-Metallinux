#  Definición básica para arrancar, después lo cambiamos

from .cpu import CPU
from .gestor_memoria import GestorMemoria
from .planificador import PlanificadorSRTF
from .proceso import Proceso

class Simulador:
    def __init__(self):
        self.reloj = 0  # Para simular el paso de tiempo
        self.cpu = CPU()
        self.gestor_memoria = GestorMemoria()
        self.planificador = PlanificadorSRTF(self.cola_listos, self.cpu)
