"""Interfaces abstractas y contratos base para las estructuras de datos lineales.
Semana 1 - Día 1: Definición de interfaces abstractas para colecciones.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Iterator


class CollectionInterface(ABC):
    """Contrato base para cualquier colección de datos manual."""

    @abstractmethod
    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la colección O(1)."""
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Determina si la colección se encuentra vacía O(1)."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Limpia todos los elementos de la colección."""
        pass


class LinkedListInterface(CollectionInterface):
    """Contrato específico para Listas Enlazadas."""

    @abstractmethod
    def append(self, data: Any) -> None:
        """Inserta un nuevo elemento al final de la lista."""
        pass

    @abstractmethod
    def prepend(self, data: Any) -> None:
        """Inserta un nuevo elemento al inicio de la lista."""
        pass

    @abstractmethod
    def remove(self, data: Any) -> bool:
        """Elimina la primera coincidencia del elemento y reconecta los punteros.
        Retorna True si fue eliminado, False si no se encontró.
        """
        pass

    @abstractmethod
    def search(self, value: Any) -> Optional[Any]:
        """Busca un valor en la lista y retorna el dato si existe."""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """Permite iterar sobre los elementos de la lista nodo a nodo."""
        pass


class StackInterface(CollectionInterface):
    """Contrato específico para Estructuras LIFO (Pilas)."""

    @abstractmethod
    def push(self, data: Any) -> None:
        """Inserta un elemento en la cima de la pila O(1)."""
        pass

    @abstractmethod
    def pop(self) -> Any:
        """Elimina y retorna el elemento en la cima de la pila O(1)."""
        pass

    @abstractmethod
    def peek(self) -> Optional[Any]:
        """Consulta el elemento en la cima sin extraerlo O(1)."""
        pass


class QueueInterface(CollectionInterface):
    """Contrato específico para Estructuras FIFO / Prioridad (Colas)."""

    @abstractmethod
    def enqueue(self, data: Any, *args: Any, **kwargs: Any) -> None:
        """Inserta un elemento en la cola."""
        pass

    @abstractmethod
    def dequeue(self) -> Optional[Any]:
        """Extrae y retorna el elemento correspondiente según la política de la cola."""
        pass

    @abstractmethod
    def peek(self) -> Optional[Any]:
        """Consulta el siguiente elemento a ser atendido sin extraerlo."""
        pass
