
import unittest
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.cpu import CPU
from core.proceso import Proceso

class TestCPU(unittest.TestCase):

    def setUp(self):
        # Configura una nueva instancia de CPU y un proceso para cada prueba.
        self.cpu = CPU()
        self.proceso = Proceso(id="P1", tamaño=100, tiempo_arribo=0, tiempo_irrupcion=5)

    def test_cpu_initialization(self):
        # Prueba que la CPU se inicializa en un estado libre."""
        self.assertIsNone(self.cpu.proceso_actual)
        self.assertTrue(self.cpu.esta_libre())

    def test_dispatch(self):
        # Prueba que el método dispatch asigna un proceso a la CPU.
        self.cpu.dispatch(self.proceso)
        self.assertFalse(self.cpu.esta_libre())
        self.assertIs(self.cpu.get_proceso_actual(), self.proceso)
        self.assertEqual(self.proceso.estado, "Ejecucion")

    def test_ejecutar_ciclo_con_proceso(self):
        # Prueba la ejecución de un ciclo de CPU con un proceso activo.
        self.cpu.dispatch(self.proceso)
        tiempo_restante_inicial = self.proceso.tiempo_restante
        
        proceso_ejecutado = self.cpu.ejecutar_ciclo()
        
        self.assertIs(proceso_ejecutado, self.proceso)
        self.assertEqual(proceso_ejecutado.tiempo_restante, tiempo_restante_inicial - 1)

    def test_ejecutar_ciclo_sin_proceso(self):
        # Prueba la ejecución de un ciclo de CPU sin ningún proceso.
        proceso_ejecutado = self.cpu.ejecutar_ciclo()
        self.assertIsNone(proceso_ejecutado)

    def test_liberar_cpu(self):
        # Prueba que el método liberar expulsa el proceso de la CPU.
        self.cpu.dispatch(self.proceso)
        proceso_liberado = self.cpu.liberar()
        
        self.assertTrue(self.cpu.esta_libre())
        self.assertIsNone(self.cpu.proceso_actual)
        self.assertIs(proceso_liberado, self.proceso)

if __name__ == '__main__':
    unittest.main()
