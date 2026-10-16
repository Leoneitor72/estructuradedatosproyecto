"""Pruebas unitarias para Semana 3:
- Lista Doblemente Enlazada Circular (step_backward, alias).
- Controlador: navegación circular y benchmark en tiempo real.
- Métricas de memoria y complejidad temporal.
"""

import unittest
from models.structures import CircularQueue, CircularDoublyLinkedList
from models.benchmarks import get_memory_footprint, run_benchmark_suite
from models.student_engine import StudentEngine
from controllers.app_controller import AppController


class TestSemana3(unittest.TestCase):
    def test_circular_doubly_linked_list_navigation(self):
        c_list = CircularDoublyLinkedList()
        c_list.enqueue("A")
        c_list.enqueue("B")
        c_list.enqueue("C")

        self.assertEqual(len(c_list), 3)
        self.assertEqual(c_list.peek(), "A")

        # Avanzar hacia adelante (step)
        next_val = c_list.step()
        self.assertEqual(next_val, "B")
        self.assertEqual(c_list.peek(), "B")

        # Retroceder hacia atrás (step_backward)
        prev_val = c_list.step_backward()
        self.assertEqual(prev_val, "A")
        self.assertEqual(c_list.peek(), "A")

    def test_controller_circular_and_benchmarks(self):
        engine = StudentEngine()
        engine.seed_sample_data()
        controller = AppController(engine)

        nodes = controller.get_circular_list_nodes()
        self.assertTrue(len(nodes) > 0)

        # Avanzar y retroceder turno en el controlador
        fwd_res = controller.avanzar_turno_circular()
        self.assertTrue(fwd_res["success"])

        bwd_res = controller.retroceder_turno_circular()
        self.assertTrue(bwd_res["success"])

        # Benchmark
        bench = controller.run_benchmarks(iterations=500)
        self.assertIn("memory", bench)
        self.assertIn("benchmarks", bench)
        self.assertEqual(bench["memory"]["node_bytes"], 48)
        self.assertTrue(len(bench["benchmarks"]) >= 5)


if __name__ == "__main__":
    unittest.main()
