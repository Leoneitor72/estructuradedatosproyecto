"""Módulo de modelos y estructuras de datos para el Sistema de Gestión de Estudiantes.
Arquitectura MVC: Capa de Modelo pura, sin dependencias de UI (Flet).
"""

from .base import CollectionInterface, LinkedListInterface, StackInterface, QueueInterface
from .structures import Node, DoublyLinkedList, Stack, PriorityQueue, CircularQueue
from .student import Estudiante, GradeList
from .undo_redo import UndoRedoManager, Action
from .student_management import StudentManager

__all__ = [
    "CollectionInterface",
    "LinkedListInterface",
    "StackInterface",
    "QueueInterface",
    "Node",
    "DoublyLinkedList",
    "Stack",
    "PriorityQueue",
    "CircularQueue",
    "Estudiante",
    "GradeList",
    "UndoRedoManager",
    "Action",
    "StudentManager",
]
