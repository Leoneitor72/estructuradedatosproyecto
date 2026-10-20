"""Pruebas unitarias para el Controlador MVC (AppController)."""

import unittest
from controllers.app_controller import AppController
from models.student_engine import StudentEngine


class TestAppController(unittest.TestCase):
    def setUp(self):
        self.engine = StudentEngine()
        self.controller = AppController(self.engine)

    def test_inscribir_and_validation(self):
        # Fallo por campos vacíos
        res = self.controller.inscribir_estudiante("", "Juan", "Perez")
        self.assertFalse(res["success"])

        # Éxito
        res2 = self.controller.inscribir_estudiante("A1", "Juan", "Perez", "15, 17, 19")
        self.assertTrue(res2["success"])
        self.assertEqual(len(self.controller.get_students_table()), 1)

        # ID duplicado
        res3 = self.controller.inscribir_estudiante("A1", "Juan2", "Perez")
        self.assertFalse(res3["success"])

    def test_undo_and_redo_events(self):
        self.assertFalse(self.controller.can_undo())
        self.assertFalse(self.controller.can_redo())

        self.controller.inscribir_estudiante("B1", "Beto", "Benitez", "14")
        self.assertTrue(self.controller.can_undo())

        undo_res = self.controller.deshacer()
        self.assertTrue(undo_res["success"])
        self.assertEqual(len(self.controller.get_students_table()), 0)
        self.assertTrue(self.controller.can_redo())

        redo_res = self.controller.rehacer()
        self.assertTrue(redo_res["success"])
        self.assertEqual(len(self.controller.get_students_table()), 1)

    def test_dar_de_baja(self):
        self.controller.inscribir_estudiante("C1", "Carla", "Castro")
        res = self.controller.dar_de_baja("C1")
        self.assertTrue(res["success"])
        self.assertEqual(len(self.controller.get_students_table()), 0)

        res_inexistente = self.controller.dar_de_baja("INEXISTENTE")
        self.assertFalse(res_inexistente["success"])

    def test_actualizar_calificaciones(self):
        self.controller.inscribir_estudiante("D1", "Diego", "Diaz", "10")
        res = self.controller.actualizar_calificaciones("D1", "18, 20")
        self.assertTrue(res["success"])
        alumno = self.controller.buscar_estudiante("D1")
        self.assertEqual(alumno["promedio"], 19.0)

    def test_priority_queue_events(self):
        self.controller.encolar_admision_prioritaria("P1", "Prioritario", "Baja", 2.0)
        self.controller.encolar_admision_prioritaria("P2", "Prioritario", "Alta", 9.0)

        items = self.controller.get_priority_queue_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["prioridad"], 9.0)

        atendido = self.controller.atender_siguiente_prioridad()
        self.assertTrue(atendido["success"])
        self.assertEqual(atendido["data"]["id"], "P2")


if __name__ == "__main__":
    unittest.main()
