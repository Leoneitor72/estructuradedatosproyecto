"""Gestor de Deshacer/Rehacer (Undo/Redo Manager) mediante Doble Pila Enlazada."""

from typing import Any, Optional, Dict
from .structures import Stack


class Action:
    """Representa una acción atómica en el sistema para poder revertirla o repetirla."""

    ADD = "ADD_STUDENT"
    REMOVE = "REMOVE_STUDENT"
    UPDATE_GRADES = "UPDATE_GRADES"

    def __init__(self, action_type: str, payload: Dict[str, Any], description: str = ""):
        self.action_type: str = action_type
        self.payload: Dict[str, Any] = payload
        self.description: str = description

    def __repr__(self) -> str:
        return f"Action(type={self.action_type}, desc='{self.description}')"


class UndoRedoManager:
    """Controlador de transacciones con dos pilas LIFO basadas en nodos:
    - undo_stack: Pila de acciones realizadas.
    - redo_stack: Pila de acciones deshechas.
    """

    def __init__(self):
        self.undo_stack: Stack = Stack()
        self.redo_stack: Stack = Stack()

    def record_action(self, action: Action) -> None:
        """Registra una nueva acción y vacía la pila de rehacer O(1)."""
        self.undo_stack.push(action)
        self.redo_stack.clear()

    def can_undo(self) -> bool:
        """Determina si hay acciones para deshacer."""
        return not self.undo_stack.is_empty()

    def can_redo(self) -> bool:
        """Determina si hay acciones para rehacer."""
        return not self.redo_stack.is_empty()

    def undo(self) -> Optional[Action]:
        """Extrae la última acción y la pasa a la pila de rehacer O(1)."""
        if not self.can_undo():
            return None
        action: Action = self.undo_stack.pop()
        self.redo_stack.push(action)
        return action

    def redo(self) -> Optional[Action]:
        """Extrae la última acción deshecha y la pasa a la pila de deshacer O(1)."""
        if not self.can_redo():
            return None
        action: Action = self.redo_stack.pop()
        self.undo_stack.push(action)
        return action

    def clear(self) -> None:
        """Limpia ambas pilas."""
        self.undo_stack.clear()
        self.redo_stack.clear()
