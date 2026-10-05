"""Entidad del dominio: Estudiante y Lista Enlazada de Calificaciones.
Cumple con la regla de NO usar arrays o listas nativas para almacenamiento interno.
"""

from typing import Optional, Iterator, Iterable, Union


class GradeNode:
    """Nodo simple para almacenar una calificación individual."""

    def __init__(self, value: float):
        self.value: float = float(value)
        self.next: Optional["GradeNode"] = None

    def __repr__(self) -> str:
        return f"GradeNode({self.value})"


class GradeList:
    """Lista enlazada simple para gestionar las calificaciones de un estudiante."""

    def __init__(self, initial_grades: Optional[Iterable[Union[int, float]]] = None):
        self.head: Optional[GradeNode] = None
        self._size: int = 0
        if initial_grades:
            for g in initial_grades:
                self.add_grade(float(g))

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    def clear(self) -> None:
        self.head = None
        self._size = 0

    def add_grade(self, grade: float) -> None:
        """Añade una calificación al final de la lista de notas."""
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
        """Calcula el promedio de las calificaciones O(n)."""
        if self._size == 0:
            return 0.0
        total = 0.0
        current = self.head
        while current:
            total += current.value
            current = current.next
        return round(total / self._size, 2)

    def to_list(self) -> list[float]:
        """Exporta las calificaciones a una lista estándar para visualización."""
        grades = []
        current = self.head
        while current:
            grades.append(current.value)
            current = current.next
        return grades

    def __iter__(self) -> Iterator[float]:
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"GradeList({self.to_list()})"


class Estudiante:
    """Entidad que representa a un estudiante según la especificación del proyecto."""

    def __init__(
        self,
        id_estudiante: str,
        nombre: str,
        apellido: str,
        calificaciones: Optional[Union[GradeList, Iterable[Union[int, float]]]] = None,
    ):
        self.id: str = str(id_estudiante).strip()
        self.nombre: str = str(nombre).strip()
        self.apellido: str = str(apellido).strip()

        if isinstance(calificaciones, GradeList):
            self.calificaciones: GradeList = calificaciones
        elif calificaciones is not None:
            self.calificaciones = GradeList(calificaciones)
        else:
            self.calificaciones = GradeList()

    def agregar_calificacion(self, nota: float) -> None:
        """Añade una nueva nota al estudiante."""
        if nota < 0.0 or nota > 100.0:
            # Rango flexible (0 a 100 o 0 a 20 según escala)
            pass
        self.calificaciones.add_grade(nota)

    def actualizar_calificaciones(self, nuevas_notas: Iterable[Union[int, float]]) -> None:
        """Reemplaza todas las calificaciones por una nueva secuencia."""
        self.calificaciones.clear()
        for nota in nuevas_notas:
            self.calificaciones.add_grade(float(nota))

    def calcular_promedio(self) -> float:
        """Calcula el promedio de calificaciones del estudiante."""
        return self.calificaciones.calculate_average()

    def to_dict(self) -> dict:
        """Retorna una representación serializable en diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "calificaciones": self.calificaciones.to_list(),
            "promedio": self.calcular_promedio(),
        }

    def __repr__(self) -> str:
        return (
            f"Estudiante(id='{self.id}', nombre='{self.nombre}', apellido='{self.apellido}', "
            f"promedio={self.calcular_promedio()})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Estudiante):
            return self.id == other.id
        return False
