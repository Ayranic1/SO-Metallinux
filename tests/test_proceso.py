
import unittest
import sys
import os

# Añadir el directorio src al path para permitir importaciones directas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.proceso import Proceso

class TestProceso(unittest.TestCase):

    def test_proceso_initialization(self):
        """Prueba que el constructor de Proceso inicializa los atributos correctamente."""
        proceso = Proceso(id="P1", tamaño=100, tiempo_arribo=0, tiempo_irrupcion=10)
        
        self.assertEqual(proceso.id, "P1")
        self.assertEqual(proceso.tamaño, 100)
        self.assertEqual(proceso.tiempo_arribo, 0)
        self.assertEqual(proceso.tiempo_irrupcion, 10)
        self.assertEqual(proceso.tiempo_restante, 10)
        self.assertEqual(proceso.estado, "Nuevo")

    def test_proceso_str_representation(self):
        """Prueba la representación en cadena de la clase Proceso."""
        proceso = Proceso(id="P2", tamaño=250, tiempo_arribo=5, tiempo_irrupcion=8)
        
        expected_str = "Proceso(P2, tamaño=250K, arribo=5, irrupción=8)"
        self.assertEqual(str(proceso), expected_str)

if __name__ == '__main__':
    unittest.main()
