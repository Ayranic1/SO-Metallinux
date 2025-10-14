
import unittest
from unittest.mock import MagicMock
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.kernel import Kernel
from core.proceso import Proceso

class TestKernel(unittest.TestCase):

    def setUp(self):
        """Configura un entorno de prueba con mocks para las dependencias del Kernel."""
        self.mock_gestor_memoria = MagicMock()
        self.mock_planificador = MagicMock()
        self.mock_gestor_colas = MagicMock()
        
        self.proceso1 = Proceso(id="P1", tamaño=100, tiempo_arribo=0, tiempo_irrupcion=5)
        self.proceso2 = Proceso(id="P2", tamaño=200, tiempo_arribo=1, tiempo_irrupcion=3)
        
        self.procesos_maestros = [self.proceso1, self.proceso2]
        
        self.kernel = Kernel(
            procesos_maestros=self.procesos_maestros,
            gestor_memoria=self.mock_gestor_memoria,
            planificador=self.mock_planificador,
            gestor_colas=self.mock_gestor_colas
        )

    def test_manejar_llegadas(self):
        """Prueba que los procesos que llegan en el tiempo actual se añaden a la cola de nuevos."""
        tiempo_actual = 0
        self.kernel.ciclo_de_trabajo(tiempo_actual)
        # Comprueba que el proceso P1 (tiempo_arribo=0) fue agregado
        self.mock_gestor_colas.agregar_nuevo.assert_called_with(self.proceso1)

        tiempo_actual = 1
        self.kernel.ciclo_de_trabajo(tiempo_actual)
        # Comprueba que el proceso P2 (tiempo_arribo=1) fue agregado
        self.mock_gestor_colas.agregar_nuevo.assert_called_with(self.proceso2)

    def test_intentar_asignar_memoria_a_nuevos(self):
        """Prueba que se intenta asignar memoria a procesos en la cola de nuevos."""
        # Simula que hay un proceso nuevo en la cola
        self.mock_gestor_colas.nuevos = [self.proceso1]
        self.mock_gestor_colas.suspendidos = []
        
        # Simula que la asignación de memoria es exitosa
        self.mock_gestor_memoria.asignar_memoria.return_value = True
        
        self.kernel._intentar_asignar_memoria()
        
        # Verifica que se intentó asignar memoria y que el proceso se movió a listos
        self.mock_gestor_memoria.asignar_memoria.assert_called_with(self.proceso1)
        self.mock_gestor_colas.mover_nuevo_a_listo.assert_called_with(self.proceso1)

    def test_manejo_proceso_terminado(self):
        """Prueba que la memoria se libera cuando un proceso termina."""
        proceso_terminado = self.proceso1
        # Simula que el planificador reporta un proceso terminado
        self.mock_planificador.manejar_finalizacion.return_value = proceso_terminado
        
        resultado = self.kernel.ciclo_de_trabajo(tiempo_actual=5)
        
        # Verifica que se liberó la memoria del proceso terminado
        self.mock_gestor_memoria.liberar_memoria.assert_called_with(proceso_terminado)
        # Verifica que el ciclo de trabajo devuelve el proceso terminado
        self.assertEqual(resultado, proceso_terminado)

if __name__ == '__main__':
    unittest.main()
