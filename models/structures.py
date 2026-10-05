"""Implementación pura de Estructuras de Datos Lineales basadas en Nodos y Punteros.
Semana 1 - Días 2, 3 y 4.
REGLA ESTRICTA: Sin uso de `list` nativo como estructura de almacenamiento subyacente.
"""

from typing import Any, Optional, Iterator, Callable
from .base import LinkedListInterface, StackInterface, QueueInterface


class Node:
    """Nodo genérico para listas y estructuras enlazadas."""

    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional["Node"] = None
        self.prev: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class PriorityNode:
    """Nodo especializado para Cola de Prioridad con punteros explícitos."""

    def __init__(self, data: Any, priority: float):
        self.data: Any = data
        self.priority: float = priority
        self.next: Optional["PriorityNode"] = None
        self.prev: Optional["PriorityNode"] = None

    def __repr__(self) -> str:
        return f"PriorityNode(data={self.data}, priority={self.priority})"


class DoublyLinkedList(LinkedListInterface):
    """Lista Doblemente Enlazada (Doubly Linked List) con punteros head y tail.
    Complejidad:
    - Inserción al inicio (prepend): O(1)
    - Inserción al final (append): O(1)
    - Búsqueda: O(n)
    - Eliminación con referencia conocida: O(1), por búsqueda: O(n)
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def clear(self) -> None:
        """Limpia los punteros asegurando la liberación de referencias."""
        current = self.head
        while current:
            next_node = current.next
            current.prev = None
            current.next = None
            current = next_node
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data: Any) -> None:
        """Inserta al final de la lista O(1)."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, data: Any) -> None:
        """Inserta al inicio de la lista O(1)."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_ordered(self, data: Any, key_func: Callable[[Any], Any]) -> None:
        """Inserta un elemento manteniendo el orden ascendente según key_func O(n)."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self._size += 1
            return

        # Si el nuevo dato es menor o igual al primero
        if key_func(data) <= key_func(self.head.data):
            self.prepend(data)
            return

        # Si el nuevo dato es mayor o igual al último
        assert self.tail is not None
        if key_func(data) >= key_func(self.tail.data):
            self.append(data)
            return

        # Inserción intermedia
        current = self.head
        while current.next and key_func(current.next.data) < key_func(data):
            current = current.next

        next_node = current.next
        new_node.next = next_node
        new_node.prev = current
        current.next = new_node
        if next_node:
            next_node.prev = new_node
        self._size += 1

    def remove(self, target: Any) -> bool:
        """Elimina un nodo que coincide con el valor o que satisface un predicado O(n).
        Reconecta cuidadosamente los punteros prev y next para evitar fugas de memoria.
        """
        current = self.head
        is_callable = callable(target)

        while current:
            matched = target(current.data) if is_callable else (current.data == target)
            if matched:
                # Caso 1: Es el único elemento
                if current == self.head and current == self.tail:
                    self.head = None
                    self.tail = None
                # Caso 2: Es la cabeza
                elif current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                # Caso 3: Es la cola
                elif current == self.tail:
                    self.tail = current.prev
                    if self.tail:
                        self.tail.next = None
                # Caso 4: Nodo intermedio
                else:
                    assert current.prev is not None
                    assert current.next is not None
                    current.prev.next = current.next
                    current.next.prev = current.prev

                # Desconectar el nodo extraído
                current.next = None
                current.prev = None
                self._size -= 1
                return True

            current = current.next

        return False

    def search(self, target: Any) -> Optional[Any]:
        """Busca un elemento por igualdad directa o mediante función predicado O(n)."""
        current = self.head
        is_callable = callable(target)
        while current:
            matched = target(current.data) if is_callable else (current.data == target)
            if matched:
                return current.data
            current = current.next
        return None

    def __iter__(self) -> Iterator[Any]:
        """Iterador manual de nodo a nodo sin usar estructuras intermedias."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def to_list(self) -> list:
        """Convierte los datos a una lista de Python para serialización o visualización."""
        return [item for item in self]


class Stack(StackInterface):
    """Pila LIFO implementada con nodos enlazados simples.
    Todas las operaciones principales son O(1).
    """

    def __init__(self):
        self.top_node: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.top_node is None

    def clear(self) -> None:
        self.top_node = None
        self._size = 0

    def push(self, data: Any) -> None:
        """Apila un elemento O(1)."""
        new_node = Node(data)
        new_node.next = self.top_node
        self.top_node = new_node
        self._size += 1

    def pop(self) -> Any:
        """Desapila el elemento superior O(1). Lanza IndexError si está vacía."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        assert self.top_node is not None
        popped_node = self.top_node
        self.top_node = popped_node.next
        popped_node.next = None
        self._size -= 1
        return popped_node.data

    def peek(self) -> Optional[Any]:
        """Observa el elemento superior sin desapilarlo O(1)."""
        if self.is_empty():
            return None
        assert self.top_node is not None
        return self.top_node.data

    def __iter__(self) -> Iterator[Any]:
        current = self.top_node
        while current:
            yield current.data
            current = current.next


class PriorityQueue(QueueInterface):
    """Cola de Prioridad implementada con nodos ordenados descendientemente.
    (Mayor número de prioridad = atendido primero).
    - Enqueue: O(n)
    - Dequeue: O(1)
    - Peek: O(1)
    """

    def __init__(self):
        self.head: Optional[PriorityNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    def clear(self) -> None:
        self.head = None
        self._size = 0

    def enqueue(self, data: Any, priority: float = 0.0) -> None:
        """Inserta un elemento manteniendo el orden de prioridad O(n)."""
        new_node = PriorityNode(data, priority)

        # Si está vacía o tiene mayor prioridad que la cabeza actual
        if not self.head or priority > self.head.priority:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.priority >= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def dequeue(self) -> Optional[Any]:
        """Extrae el elemento de mayor prioridad O(1)."""
        if self.is_empty():
            return None
        assert self.head is not None
        value = self.head.data
        self.head = self.head.next
        self._size -= 1
        return value

    def peek(self) -> Optional[Any]:
        """Consulta el dato del elemento con mayor prioridad sin extraerlo O(1)."""
        if self.is_empty():
            return None
        assert self.head is not None
        return self.head.data

    def peek_priority(self) -> Optional[float]:
        """Consulta el valor numérico de la prioridad más alta O(1)."""
        if self.is_empty():
            return None
        assert self.head is not None
        return self.head.priority

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield (current.data, current.priority)
            current = current.next


class CircularQueue(QueueInterface):
    """Cola Circular / Lista Enlazada Circular con punteros tail.next = head.
    Permite procesamiento por turnos cíclicos (Round-Robin).
    - Enqueue: O(1)
    - Dequeue: O(1)
    - Step / Advance: O(1)
    """

    def __init__(self, capacity: Optional[int] = None):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.capacity: Optional[int] = capacity
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        if self.capacity is None:
            return False
        return self._size >= self.capacity

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, data: Any) -> None:
        """Añade un elemento al final de la cola circular O(1)."""
        if self.is_full():
            raise OverflowError("CircularQueue is full")

        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
            new_node.prev = self.tail
        else:
            assert self.tail is not None
            assert self.head is not None
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

        self._size += 1

    def dequeue(self) -> Optional[Any]:
        """Extrae el elemento del frente de la cola circular O(1)."""
        if self.is_empty():
            return None

        assert self.head is not None
        assert self.tail is not None

        value = self.head.data
        if self._size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            assert self.head is not None
            self.head.prev = self.tail
            self.tail.next = self.head

        self._size -= 1
        return value

    def peek(self) -> Optional[Any]:
        """Consulta el elemento frontal O(1)."""
        if self.is_empty():
            return None
        assert self.head is not None
        return self.head.data

    def step(self) -> Optional[Any]:
        """Avanza un paso en el ciclo (el head pasa a ser tail y tail.next pasa a ser head) O(1).
        Retorna el nuevo elemento que queda al frente.
        """
        if self.is_empty() or self._size == 1:
            return self.peek()

        assert self.head is not None
        assert self.tail is not None
        self.tail = self.head
        self.head = self.head.next
        return self.head.data

    def __iter__(self) -> Iterator[Any]:
        """Itera una vuelta completa por los elementos circulares."""
        if self.is_empty():
            return
        current = self.head
        for _ in range(self._size):
            assert current is not None
            yield current.data
            current = current.next
