"""=============================================================================
PROYECTO: SISTEMA DE GESTION DE ESTUDIANTES (SEMANA 1)
CURSO: Estructuras de Datos y Algoritmos
PATRON: Arquitectura basada en Nodos y Punteros Manuales (Sin listas nativas)
=============================================================================
"""

from typing import Optional, Iterator, Callable, Any, List, Dict


# =============================================================================
# 1. ESTRUCTURAS DE DATOS LINEALES PURAS (MANEJO MANUAL DE PUNTEROS)
# =============================================================================

class Node:
    """Nodo fundamental con punteros bidireccionales."""
    def __init__(self, data: Any):
        self.data: Any = data
        self.next: Optional["Node"] = None
        self.prev: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class DoublyLinkedList:
    """Lista Doblemente Enlazada manual (Cumple la regla: 0% uso de list de Python)."""
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def append(self, data: Any) -> None:
        """Inserta al final O(1)."""
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
        """Inserta al inicio O(1)."""
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
        """Inserta ordenado segun criterio (ID o Apellido) O(n)."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self._size += 1
            return

        if key_func(data) <= key_func(self.head.data):
            self.prepend(data)
            return

        assert self.tail is not None
        if key_func(data) >= key_func(self.tail.data):
            self.append(data)
            return

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

    def remove(self, predicate: Callable[[Any], bool]) -> bool:
        """Elimina reconectando punteros prev y next sin fugas de memoria O(n)."""
        current = self.head
        while current:
            if predicate(current.data):
                if current == self.head and current == self.tail:
                    self.head = None
                    self.tail = None
                elif current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                elif current == self.tail:
                    self.tail = current.prev
                    if self.tail:
                        self.tail.next = None
                else:
                    assert current.prev is not None
                    assert current.next is not None
                    current.prev.next = current.next
                    current.next.prev = current.prev

                current.next = None
                current.prev = None
                self._size -= 1
                return True
            current = current.next
        return False

    def search(self, predicate: Callable[[Any], bool]) -> Optional[Any]:
        """Busqueda lineal sobre punteros O(n)."""
        current = self.head
        while current:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def __iter__(self) -> Iterator[Any]:
        """Iterador manual de nodo a nodo."""
        current = self.head
        while current:
            yield current.data
            current = current.next


class Stack:
    """Pila LIFO implementada con nodos enlazados O(1)."""
    def __init__(self):
        self.top_node: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.top_node is None

    def push(self, data: Any) -> None:
        new_node = Node(data)
        new_node.next = self.top_node
        self.top_node = new_node
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        assert self.top_node is not None
        node = self.top_node
        self.top_node = node.next
        node.next = None
        self._size -= 1
        return node.data

    def peek(self) -> Optional[Any]:
        return self.top_node.data if self.top_node else None

    def clear(self) -> None:
        self.top_node = None
        self._size = 0


# =============================================================================
# 2. ENTIDAD ESTUDIANTE Y LISTA ENLAZADA DE CALIFICACIONES
# =============================================================================

class GradeNode:
    """Nodo para una calificacion individual."""
    def __init__(self, value: float):
        self.value: float = float(value)
        self.next: Optional["GradeNode"] = None


class GradeList:
    """Lista enlazada propia para notas (incluso las notas son manuales)."""
    def __init__(self, grades: Optional[List[float]] = None):
        self.head: Optional[GradeNode] = None
        self._size: int = 0
        if grades:
            for g in grades:
                self.add_grade(float(g))

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self.head = None
        self._size = 0

    def add_grade(self, grade: float) -> None:
        new_node = GradeNode(grade)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def calculate_average(self) -> float:
        if self._size == 0:
            return 0.0
        total = 0.0
        current = self.head
        while current:
            total += current.value
            current = current.next
        return round(total / self._size, 2)

    def __iter__(self) -> Iterator[float]:
        current = self.head
        while current:
            yield current.value
            current = current.next

    def to_list(self) -> List[float]:
        return [g for g in self]


class Estudiante:
    """Entidad Estudiante que se encapsula dentro del nodo de la lista."""
    def __init__(self, id_estudiante: str, nombre: str, apellido: str, notas: Optional[List[float]] = None):
        self.id: str = str(id_estudiante).strip()
        self.nombre: str = str(nombre).strip()
        self.apellido: str = str(apellido).strip()
        self.calificaciones: GradeList = GradeList(notas)

    def calcular_promedio(self) -> float:
        return self.calificaciones.calculate_average()

    def actualizar_calificaciones(self, nuevas_notas: List[float]) -> None:
        self.calificaciones.clear()
        for n in nuevas_notas:
            self.calificaciones.add_grade(float(n))

    def __repr__(self) -> str:
        return f"{self.id} | {self.apellido}, {self.nombre} | Promedio: {self.calcular_promedio():.2f}"


# =============================================================================
# 3. GESTOR UNDO/REDO MEDIANTE DOBLE PILA
# =============================================================================

class Action:
    ADD = "ADD"
    REMOVE = "REMOVE"
    UPDATE = "UPDATE"

    def __init__(self, action_type: str, payload: Dict[str, Any]):
        self.action_type: str = action_type
        self.payload: Dict[str, Any] = payload


class UndoRedoManager:
    """Manejo de transacciones reversibles mediante dos pilas acopladas."""
    def __init__(self):
        self.undo_stack: Stack = Stack()
        self.redo_stack: Stack = Stack()

    def record(self, action: Action) -> None:
        self.undo_stack.push(action)
        self.redo_stack.clear()

    def undo(self) -> Optional[Action]:
        if self.undo_stack.is_empty():
            return None
        action = self.undo_stack.pop()
        self.redo_stack.push(action)
        return action

    def redo(self) -> Optional[Action]:
        if self.redo_stack.is_empty():
            return None
        action = self.redo_stack.pop()
        self.undo_stack.push(action)
        return action


# =============================================================================
# 4. SISTEMA DE GESTION DE ESTUDIANTES (LAS 5 FUNCIONALIDADES)
# =============================================================================

class StudentManager:
    """Motor de gestion de estudiantes sobre la Lista Doblemente Enlazada."""
    def __init__(self, sort_by: Optional[str] = "apellido"):
        self.students: DoublyLinkedList = DoublyLinkedList()
        self.history: UndoRedoManager = UndoRedoManager()
        self.sort_by: Optional[str] = sort_by

    # FUNCIONALIDAD 1: Inscribir Estudiante
    def inscribir_estudiante(self, id_est: str, nombre: str, apellido: str, notas: Optional[List[float]] = None) -> Estudiante:
        id_clean = str(id_est).strip()
        if self.buscar_estudiante(id_clean):
            raise ValueError(f"Ya existe un alumno con ID: {id_clean}")

        est = Estudiante(id_clean, nombre, apellido, notas)
        if self.sort_by == "apellido":
            self.students.insert_ordered(est, key_func=lambda e: (e.apellido.lower(), e.nombre.lower()))
        elif self.sort_by == "id":
            self.students.insert_ordered(est, key_func=lambda e: e.id)
        else:
            self.students.append(est)

        self.history.record(Action(Action.ADD, {"estudiante": est}))
        return est

    # FUNCIONALIDAD 2: Dar de Baja a Estudiante por ID
    def dar_de_baja(self, id_est: str) -> bool:
        id_clean = str(id_est).strip()
        est = self.buscar_estudiante(id_clean)
        if not est:
            return False

        notas_previas = est.calificaciones.to_list()
        eliminado = self.students.remove(lambda e: e.id == id_clean)
        if eliminado:
            self.history.record(Action(Action.REMOVE, {
                "id": est.id, "nombre": est.nombre, "apellido": est.apellido, "notas": notas_previas
            }))
        return eliminado

    # FUNCIONALIDAD 3: Actualizar Calificaciones
    def actualizar_calificaciones(self, id_est: str, nuevas_notas: List[float]) -> bool:
        est = self.buscar_estudiante(id_est)
        if not est:
            return False
        viejas_notas = est.calificaciones.to_list()
        est.actualizar_calificaciones(nuevas_notas)
        self.history.record(Action(Action.UPDATE, {
            "id": est.id, "old_grades": viejas_notas, "new_grades": nuevas_notas
        }))
        return True

    # FUNCIONALIDAD 4: Calcular Promedio
    def calcular_promedio(self, id_est: str) -> Optional[float]:
        est = self.buscar_estudiante(id_est)
        return est.calcular_promedio() if est else None

    def buscar_estudiante(self, id_est: str) -> Optional[Estudiante]:
        id_clean = str(id_est).strip()
        return self.students.search(lambda e: e.id == id_clean)

    # FUNCIONALIDAD 5: Generar Reporte
    def generar_reporte(self) -> None:
        print("\n" + "=" * 70)
        print(f"{'ID':<10} | {'APELLIDO':<15} | {'NOMBRE':<15} | {'PROMEDIO':<8} | NOTAS")
        print("-" * 70)
        if self.students.is_empty():
            print("  (No hay estudiantes registrados)")
        else:
            for est in self.students:
                notas_str = ", ".join(f"{g:.1f}" for g in est.calificaciones) or "Sin notas"
                print(f"{est.id:<10} | {est.apellido:<15} | {est.nombre:<15} | {est.calcular_promedio():<8.2f} | {notas_str}")
        print("=" * 70)
        print(f"Total inscritos en lista enlazada: {len(self.students)}")

    # GESTION UNDO / REDO (Deshacer y Rehacer)
    def deshacer(self) -> Optional[str]:
        action = self.history.undo()
        if not action:
            return "Nada que deshacer."

        if action.action_type == Action.ADD:
            est = action.payload["estudiante"]
            self.students.remove(lambda e: e.id == est.id)
            return f"Deshecho: Se removio inscripcion de {est.id}"
        elif action.action_type == Action.REMOVE:
            p = action.payload
            restaurado = Estudiante(p["id"], p["nombre"], p["apellido"], p["notas"])
            self.students.insert_ordered(restaurado, key_func=lambda e: (e.apellido.lower(), e.nombre.lower()))
            return f"Deshecho: Se restauro al alumno {p['id']}"
        elif action.action_type == Action.UPDATE:
            p = action.payload
            est = self.buscar_estudiante(p["id"])
            if est:
                est.actualizar_calificaciones(p["old_grades"])
            return f"Deshecho: Se restauraron notas anteriores de {p['id']}"
        return None

    def rehacer(self) -> Optional[str]:
        action = self.history.redo()
        if not action:
            return "Nada que rehacer."

        if action.action_type == Action.ADD:
            est = action.payload["estudiante"]
            self.students.insert_ordered(est, key_func=lambda e: (e.apellido.lower(), e.nombre.lower()))
            return f"Rehecho: Se reinscribio a {est.id}"
        elif action.action_type == Action.REMOVE:
            p = action.payload
            self.students.remove(lambda e: e.id == p["id"])
            return f"Rehecho: Se volvio a dar de baja a {p['id']}"
        elif action.action_type == Action.UPDATE:
            p = action.payload
            est = self.buscar_estudiante(p["id"])
            if est:
                est.actualizar_calificaciones(p["new_grades"])
            return f"Rehecho: Se volvieron a aplicar notas nuevas a {p['id']}"
        return None


# =============================================================================
# 5. DEMOSTRACION EN VIVO PARA LA PRESENTACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" DEMOSTRACION SEMANA 1: SISTEMA DE GESTION DE ESTUDIANTES")
    print(" IMPLEMENTACION PURA CON NODOS Y PUNTEROS (DOUBLY LINKED LIST)")
    print("=" * 70)

    # 1. Instanciacion
    manager = StudentManager(sort_by="apellido")

    # 2. Funcionalidad 1: Inscribir
    print("\n[Paso 1] Inscribiendo 4 estudiantes...")
    manager.inscribir_estudiante("EST-101", "Maria", "Gonzalez", [18.0, 19.5, 17.0])
    manager.inscribir_estudiante("EST-102", "Alejandro", "Barrios", [14.0, 15.0, 13.5])
    manager.inscribir_estudiante("EST-103", "Camila", "Diaz", [20.0, 19.0, 18.5])
    manager.inscribir_estudiante("EST-104", "Esteban", "Torres", [12.0, 11.0, 10.5])
    print("[OK] Alumnos inscritos e insertados ordenados por apellido.")

    # 3. Funcionalidad 5: Reporte inicial
    manager.generar_reporte()

    # 4. Funcionalidad 4: Calcular Promedio
    print(f"\n[Paso 2] Promedio calculado para EST-103: {manager.calcular_promedio('EST-103'):.2f}")

    # 5. Funcionalidad 3: Actualizar notas
    print("\n[Paso 3] Modificando calificaciones de EST-104 a [16.0, 18.0, 19.0]...")
    manager.actualizar_calificaciones("EST-104", [16.0, 18.0, 19.0])
    print(f"[OK] Nuevo promedio de EST-104: {manager.calcular_promedio('EST-104'):.2f}")

    # 6. Funcionalidad 2: Dar de baja por ID
    print("\n[Paso 4] Dando de baja a EST-102 (Alejandro Barrios)...")
    manager.dar_de_baja("EST-102")
    manager.generar_reporte()

    # 7. Deshacer y Rehacer (Undo / Redo)
    print("\n[Paso 5] Probando Undo (Deshacer la baja de EST-102):")
    print(manager.deshacer())
    manager.generar_reporte()

    print("\n[Paso 6] Probando Redo (Rehacer la baja):")
    print(manager.rehacer())
    manager.generar_reporte()

    print("\n" + "=" * 70)
    print(" FIN DE LA DEMOSTRACION - SEMANA 1 COMPLETA")
    print("=" * 70)
