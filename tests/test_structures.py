"""Pruebas unitarias para las Estructuras de Datos Lineales.
Valida el manejo explícito de nodos, consistencia de punteros bidireccionales y casos límite.
"""

import unittest
from models.structures import Node, DoublyLinkedList, Stack, PriorityQueue, CircularQueue


class TestDoublyLinkedList(unittest.TestCase):
    """Pruebas exhaustivas para la Lista Doblemente Enlazada."""

    def setUp(self):
        self.dll = DoublyLinkedList()

    def _assert_pointer_integrity(self, dll: DoublyLinkedList):
        """Verifica que cada nodo apunte correctamente hacia adelante y atrás."""
        if dll.is_empty():
            self.assertIsNone(dll.head)
            self.assertIsNone(dll.tail)
            return

        # Cabeza no debe tener prev
        self.assertIsNone(dll.head.prev)
        # Cola no debe tener next
        self.assertIsNone(dll.tail.next)

        current = dll.head
        count = 0
        last = None
        while current:
            count += 1
            if current.prev is not None:
                self.assertIs(current.prev.next, current, "El puntero prev.next no coincide con el nodo")
            if current.next is not None:
                self.assertIs(current.next.prev, current, "El puntero next.prev no coincide con el nodo")
            last = current
            current = current.next

        self.assertEqual(count, len(dll))
        self.assertIs(last, dll.tail)

    def test_empty_list(self):
        self.assertTrue(self.dll.is_empty())
        self.assertEqual(len(self.dll), 0)
        self.assertIsNone(self.dll.head)
        self.assertIsNone(self.dll.tail)
        self.assertFalse(self.dll.remove("inexistente"))
        self.assertIsNone(self.dll.search("inexistente"))

    def test_append_single_and_multiple(self):
        self.dll.append(10)
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.head.data, 10)
        self.assertEqual(self.dll.tail.data, 10)
        self._assert_pointer_integrity(self.dll)

        self.dll.append(20)
        self.dll.append(30)
        self.assertEqual(len(self.dll), 3)
        self.assertEqual(self.dll.to_list(), [10, 20, 30])
        self._assert_pointer_integrity(self.dll)

    def test_prepend(self):
        self.dll.prepend(30)
        self.dll.prepend(20)
        self.dll.prepend(10)
        self.assertEqual(self.dll.to_list(), [10, 20, 30])
        self._assert_pointer_integrity(self.dll)

    def test_insert_ordered(self):
        self.dll.insert_ordered(30, key_func=lambda x: x)
        self.dll.insert_ordered(10, key_func=lambda x: x)
        self.dll.insert_ordered(20, key_func=lambda x: x)
        self.dll.insert_ordered(40, key_func=lambda x: x)
        self.dll.insert_ordered(5, key_func=lambda x: x)
        self.assertEqual(self.dll.to_list(), [5, 10, 20, 30, 40])
        self._assert_pointer_integrity(self.dll)

    def test_remove_cases(self):
        # 1. Caso un solo elemento
        self.dll.append(100)
        self.assertTrue(self.dll.remove(100))
        self.assertTrue(self.dll.is_empty())
        self._assert_pointer_integrity(self.dll)

        # 2. Caso eliminar cabeza
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)
        self.assertTrue(self.dll.remove(1))
        self.assertEqual(self.dll.to_list(), [2, 3])
        self.assertEqual(self.dll.head.data, 2)
        self._assert_pointer_integrity(self.dll)

        # 3. Caso eliminar cola
        self.assertTrue(self.dll.remove(3))
        self.assertEqual(self.dll.to_list(), [2])
        self.assertEqual(self.dll.tail.data, 2)
        self._assert_pointer_integrity(self.dll)

        # 4. Caso eliminar intermedio
        self.dll.clear()
        self.dll.append("A")
        self.dll.append("B")
        self.dll.append("C")
        self.assertTrue(self.dll.remove("B"))
        self.assertEqual(self.dll.to_list(), ["A", "C"])
        self.assertEqual(self.dll.head.next.data, "C")
        self.assertEqual(self.dll.tail.prev.data, "A")
        self._assert_pointer_integrity(self.dll)

    def test_search(self):
        self.dll.append("Alice")
        self.dll.append("Bob")
        self.dll.append("Charlie")

        found = self.dll.search(lambda x: x == "Bob")
        self.assertEqual(found, "Bob")

        not_found = self.dll.search(lambda x: x == "David")
        self.assertIsNone(not_found)

    def test_clear(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.clear()
        self.assertEqual(len(self.dll), 0)
        self.assertTrue(self.dll.is_empty())
        self.assertIsNone(self.dll.head)
        self.assertIsNone(self.dll.tail)


class TestStack(unittest.TestCase):
    """Pruebas para la Pila (Stack) LIFO."""

    def setUp(self):
        self.stack = Stack()

    def test_stack_operations(self):
        self.assertTrue(self.stack.is_empty())
        self.assertIsNone(self.stack.peek())

        # Push
        self.stack.push("Action 1")
        self.stack.push("Action 2")
        self.assertEqual(len(self.stack), 2)
        self.assertEqual(self.stack.peek(), "Action 2")

        # Pop
        popped = self.stack.pop()
        self.assertEqual(popped, "Action 2")
        self.assertEqual(len(self.stack), 1)
        self.assertEqual(self.stack.peek(), "Action 1")

        popped2 = self.stack.pop()
        self.assertEqual(popped2, "Action 1")
        self.assertTrue(self.stack.is_empty())

        # Pop on empty stack
        with self.assertRaises(IndexError):
            self.stack.pop()


class TestPriorityQueue(unittest.TestCase):
    """Pruebas para la Cola de Prioridad."""

    def setUp(self):
        self.pq = PriorityQueue()

    def test_priority_ordering(self):
        self.assertTrue(self.pq.is_empty())
        self.assertIsNone(self.pq.dequeue())

        self.pq.enqueue("Tarea Normal", priority=1.0)
        self.pq.enqueue("Tarea Urgente VIP", priority=5.0)
        self.pq.enqueue("Tarea Media", priority=3.0)
        self.pq.enqueue("Tarea Muy Baja", priority=0.5)

        self.assertEqual(len(self.pq), 4)
        self.assertEqual(self.pq.peek(), "Tarea Urgente VIP")
        self.assertEqual(self.pq.peek_priority(), 5.0)

        # Dequeue en orden estricto de mayor a menor
        self.assertEqual(self.pq.dequeue(), "Tarea Urgente VIP")
        self.assertEqual(self.pq.dequeue(), "Tarea Media")
        self.assertEqual(self.pq.dequeue(), "Tarea Normal")
        self.assertEqual(self.pq.dequeue(), "Tarea Muy Baja")
        self.assertTrue(self.pq.is_empty())


class TestCircularQueue(unittest.TestCase):
    """Pruebas para la Cola Circular (Round-Robin)."""

    def setUp(self):
        self.cq = CircularQueue(capacity=5)

    def test_circular_behavior(self):
        self.assertTrue(self.cq.is_empty())

        self.cq.enqueue("Item 1")
        self.cq.enqueue("Item 2")
        self.cq.enqueue("Item 3")
        self.assertEqual(len(self.cq), 3)

        # Verificar punteros circulares
        self.assertIs(self.cq.tail.next, self.cq.head)
        self.assertIs(self.cq.head.prev, self.cq.tail)

        # Step / Round-Robin
        next_item = self.cq.step()
        self.assertEqual(next_item, "Item 2")
        self.assertEqual(self.cq.peek(), "Item 2")

        # Dequeue
        val = self.cq.dequeue()
        self.assertEqual(val, "Item 2")
        self.assertEqual(len(self.cq), 2)


if __name__ == "__main__":
    unittest.main()
