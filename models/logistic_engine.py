"""Alias pedagógico y de compatibilidad con la propuesta de rúbrica.
En el dominio de Gestión de Estudiantes, opera como interfaz directa hacia StudentEngine.
"""

from .student_engine import StudentEngine

# Exportación principal para coincidir con el nombre del módulo en la rúbrica del PDF
LogisticEngine = StudentEngine
__all__ = ["LogisticEngine", "StudentEngine"]
