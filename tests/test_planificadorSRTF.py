
import unittest
from unittest.mock import MagicMock, PropertyMock
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.planificadorSRTF import PlanificadorSRTF
from core.proceso import Proceso

class TestPlanificadorSRTF(unittest.TestCase):

    def setUp(self):
        """Configura mocks para GestorColas y CPU antes de cada prueba."""
        self.mock_gestor_colas = MagicMock()
        self.mock_cpu = MagicMock()
        self.planificador = PlanificadorSRTF(self.mock_gestor_colas, self.mock_cpu)

    def test_seleccionar_proximo_proceso_listo(self):
        """Prueba que se selecciona el proceso con el menor tiempo restante."""
        p1 = Proceso("P1", 50, 0, 10)
        p2 = Proceso("P2", 50, 0, 5) # Menor tiempo restante
        p3 = Proceso("P3", 50, 0, 8)
        self.mock_gestor_colas.listos = [p1, p2, p3]

        proceso_seleccionado = self.planificador.seleccionar_proximo_proceso_listo()
        self.assertIs(proceso_seleccionado, p2)

    def test_seleccionar_sin_procesos_listos(self):
        """Prueba que no se selecciona nada si la cola de listos está vacía."""
        self.mock_gestor_colas.listos = []
        proceso_seleccionado = self.planificador.seleccionar_proximo_proceso_listo()
        self.assertIsNone(proceso_seleccionado)

    def test_preempcion_necesaria(self):
        """Prueba que la preempción se detecta correctamente."""
        proceso_en_cpu = Proceso("CPU_P", 100, 0, 20)
        proceso_listo = Proceso("LISTO_P", 100, 1, 10) # Menor tiempo restante
        
        self.mock_cpu.get_proceso_actual.return_value = proceso_en_cpu
        self.mock_gestor_colas.listos = [proceso_listo]
        
        # Mock para seleccionar_proximo_proceso_listo devuelva el proceso listo
        self.planificador.seleccionar_proximo_proceso_listo = MagicMock(return_value=proceso_listo)

        self.assertTrue(self.planificador._necesita_preempcion())

    def test_preempcion_no_necesaria(self):
        """Prueba que no se requiere preempción si el proceso en CPU es más corto."""
        proceso_en_cpu = Proceso("CPU_P", 100, 0, 5)
        proceso_listo = Proceso("LISTO_P", 100, 1, 15)

        self.mock_cpu.get_proceso_actual.return_value = proceso_en_cpu
        self.mock_gestor_colas.listos = [proceso_listo]

        self.planificador.seleccionar_proximo_proceso_listo = MagicMock(return_value=proceso_listo)

        self.assertFalse(self.planificador._necesita_preempcion())

    def test_preemptar(self):
        """Prueba que el proceso desalojado de la CPU vuelve a la cola de listos."""
        proceso_desalojado = Proceso("P_OUT", 100, 0, 15)
        self.mock_cpu.liberar.return_value = proceso_desalojado
        self.mock_gestor_colas.listos = [] # Inicia vacía

        self.planificador._preemptar()

        self.mock_cpu.liberar.assert_called_once()
        self.assertEqual(proceso_desalojado.estado, "Listo")
        self.assertIn(proceso_desalojado, self.mock_gestor_colas.listos)

if __name__ == '__main__':
    unittest.main()
