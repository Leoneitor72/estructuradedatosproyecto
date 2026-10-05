"""Pruebas unitarias para el Sistema de Gestión de Estudiantes.
Semana 1 - Día 5.
Verifica las 5 funcionalidades requeridas y las capacidades de Undo/Redo y Colas.
"""

import unittest
from models.student import Estudiante, GradeList
from models.student_management import StudentManager
from models.undo_redo import Action


class TestStudentModel(unittest.TestCase):
    """Pruebas para la clase Estudiante y la lista enlazada GradeList."""

    def test_grade_list_and_average(self):
        grades = GradeList()
        self.assertEqual(grades.calculate_average(), 0.0)

        grades.add_grade(15.0)
        grades.add_grade(17.5)
        grades.add_grade(12.5)

        self.assertEqual(len(grades), 3)
        self.assertEqual(grades.calculate_average(), 15.0)
        self.assertEqual(grades.to_list(), [15.0, 17.5, 12.5])

    def test_student_creation_and_update(self):
        est = Estudiante("EST-001", "Carlos", "Perez", [14, 16, 18])
        self.assertEqual(est.id, "EST-001")
        self.assertEqual(est.nombre, "Carlos")
        self.assertEqual(est.apellido, "Perez")
        self.assertEqual(est.calcular_promedio(), 16.0)

        est.actualizar_calificaciones([20, 20])
        self.assertEqual(est.calcular_promedio(), 20.0)
        self.assertEqual(est.calificaciones.to_list(), [20.0, 20.0])


class TestStudentManager(unittest.TestCase):
    """Pruebas de las 5 funcionalidades clave del Sistema de Gestión de Estudiantes."""

    def setUp(self):
        self.manager = StudentManager()

    def test_1_inscribir_estudiante(self):
        """Funcionalidad 1: Inscribir Estudiante."""
        est = self.manager.inscribir_estudiante("A101", "Ana", "Gomez", [18, 19])
        self.assertIsNotNone(est)
        self.assertEqual(len(self.manager.students_list), 1)

        # Buscarlo en la lista
        buscado = self.manager.buscar_estudiante("A101")
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.nombre, "Ana")

        # Evitar ID duplicado
        with self.assertRaises(ValueError):
            self.manager.inscribir_estudiante("A101", "Ana Duplicada", "Gomez")

    def test_inscribir_ordenado_por_apellido(self):
        manager_ord = StudentManager(sort_by="apellido")
        manager_ord.inscribir_estudiante("3", "Pedro", "Zapata")
        manager_ord.inscribir_estudiante("1", "Maria", "Alvarez")
        manager_ord.inscribir_estudiante("2", "Luis", "Mendez")

        reporte = manager_ord.generar_reporte()
        apellidos = [item["apellido"] for item in reporte]
        self.assertEqual(apellidos, ["Alvarez", "Mendez", "Zapata"])

    def test_2_dar_de_baja(self):
        """Funcionalidad 2: Dar de Baja a Estudiante por ID."""
        self.manager.inscribir_estudiante("B202", "Bernardo", "Reyes", [12, 14])
        self.assertEqual(len(self.manager.students_list), 1)

        # Dar de baja existente
        eliminado = self.manager.dar_de_baja("B202")
        self.assertTrue(eliminado)
        self.assertEqual(len(self.manager.students_list), 0)
        self.assertIsNone(self.manager.buscar_estudiante("B202"))

        # Intentar dar de baja inexistente
        self.assertFalse(self.manager.dar_de_baja("INEXISTENTE"))

    def test_3_actualizar_calificaciones(self):
        """Funcionalidad 3: Actualizar Calificaciones."""
        self.manager.inscribir_estudiante("C303", "Clara", "Lara", [10, 10])
        self.assertEqual(self.manager.calcular_promedio("C303"), 10.0)

        # Modificar sus notas
        actualizado = self.manager.actualizar_calificaciones("C303", [18, 20])
        self.assertTrue(actualizado)
        self.assertEqual(self.manager.calcular_promedio("C303"), 19.0)

        # Actualizar estudiante inexistente
        self.assertFalse(self.manager.actualizar_calificaciones("FALSO", [20]))

    def test_4_calcular_promedio(self):
        """Funcionalidad 4: Calcular Promedio."""
        self.manager.inscribir_estudiante("D404", "Daniel", "Duarte", [15, 17, 19])
        promedio = self.manager.calcular_promedio("D404")
        self.assertEqual(promedio, 17.0)

        # Estudiante sin notas
        self.manager.inscribir_estudiante("D405", "David", "Diaz")
        self.assertEqual(self.manager.calcular_promedio("D405"), 0.0)

        # Inexistente
        self.assertIsNone(self.manager.calcular_promedio("INEXISTENTE"))

    def test_5_generar_reporte(self):
        """Funcionalidad 5: Generar Reporte con lista completa de estudiantes."""
        self.manager.inscribir_estudiante("E1", "Elena", "Vega", [16, 18])
        self.manager.inscribir_estudiante("E2", "Esteban", "Torres", [12, 14])

        reporte = self.manager.generar_reporte()
        self.assertEqual(len(reporte), 2)
        self.assertEqual(reporte[0]["id"], "E1")
        self.assertEqual(reporte[0]["promedio"], 17.0)
        self.assertEqual(reporte[1]["id"], "E2")
        self.assertEqual(reporte[1]["promedio"], 13.0)

        # Reporte de texto formateado
        reporte_str = self.manager.generar_reporte_texto()
        self.assertIn("Elena", reporte_str)
        self.assertIn("Esteban", reporte_str)

    def test_undo_and_redo_workflow(self):
        """Prueba del gestor Undo/Redo mediante doble pila."""
        # Inscribir
        self.manager.inscribir_estudiante("U1", "Unai", "Solis", [15])
        self.assertEqual(len(self.manager.students_list), 1)

        # Deshacer inscripción
        self.manager.deshacer()
        self.assertEqual(len(self.manager.students_list), 0)

        # Rehacer inscripción
        self.manager.rehacer()
        self.assertEqual(len(self.manager.students_list), 1)
        self.assertIsNotNone(self.manager.buscar_estudiante("U1"))

        # Dar de baja y deshacer la baja
        self.manager.dar_de_baja("U1")
        self.assertEqual(len(self.manager.students_list), 0)

        self.manager.deshacer()
        self.assertEqual(len(self.manager.students_list), 1)
        restaurado = self.manager.buscar_estudiante("U1")
        self.assertIsNotNone(restaurado)
        self.assertEqual(restaurado.calificaciones.to_list(), [15.0])

    def test_priority_queue_and_circular_review(self):
        """Prueba de Colas de Prioridad y Circular."""
        est_normal = Estudiante("N1", "Normal", "User")
        est_vip = Estudiante("V1", "VIP", "Scholarship")

        self.manager.encolar_solicitud_prioritaria(est_normal, prioridad=1.0)
        self.manager.encolar_solicitud_prioritaria(est_vip, prioridad=10.0)

        atendido = self.manager.atender_siguiente_solicitud()
        self.assertEqual(atendido.id, "V1")

        # Cargar ronda circular
        self.manager.inscribir_estudiante("R1", "A", "A")
        self.manager.inscribir_estudiante("R2", "B", "B")
        self.manager.cargar_ronda_circular()

        turno1 = self.manager.siguiente_en_turno()
        self.assertEqual(turno1.id, "R2")


if __name__ == "__main__":
    unittest.main()
