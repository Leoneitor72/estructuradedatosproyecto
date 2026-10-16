"""Motor Lógico del Dominio de Estudiantes y Estructuras de Datos.
Semana 2 - Día 1: Integración del motor de negocio con entidades y estructuras.
Extiende y provee utilidades de inspección para la capa de Controladores y Vistas.
"""

from typing import List, Dict, Any, Optional
from .student_management import StudentManager
from .student import Estudiante
from .structures import DoublyLinkedList, Stack, PriorityQueue, CircularQueue
from .undo_redo import UndoRedoManager


class StudentEngine(StudentManager):
    """Motor de gestión de estudiantes con capacidades analíticas y de inspección para la UI."""

    def __init__(self, sort_by: Optional[str] = "apellido"):
        super().__init__(sort_by=sort_by)

    def seed_sample_data(self) -> None:
        """Carga datos de prueba para visualización inmediata en la interfaz."""
        if not self.students_list.is_empty():
            return

        # Estudiantes iniciales con notas
        self.inscribir_estudiante("EST-101", "Maria", "Gonzalez", [18.5, 19.0, 17.5], record_history=False)
        self.inscribir_estudiante("EST-102", "Alejandro", "Barrios", [14.0, 15.5, 13.0], record_history=False)
        self.inscribir_estudiante("EST-103", "Camila", "Diaz", [20.0, 19.5, 19.0], record_history=False)
        self.inscribir_estudiante("EST-104", "Esteban", "Torres", [11.0, 12.5, 10.5], record_history=False)

        # Cargar cola circular con los inscritos
        self.cargar_ronda_circular()

        # Solicitudes prioritarias de prueba
        self.encolar_solicitud_prioritaria(
            Estudiante("SOL-01", "Javier", "Paz (Beca Excelencia)", [19.0, 20.0]),
            prioridad=9.5
        )
        self.encolar_solicitud_prioritaria(
            Estudiante("SOL-02", "Andres", "Ruiz (Reubicacion)", [15.0, 16.0]),
            prioridad=6.0
        )
        self.encolar_solicitud_prioritaria(
            Estudiante("SOL-03", "Lucia", "Mendez (Regular)", [13.0, 14.0]),
            prioridad=2.5
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Calcula estadísticas generales del centro educativo O(n)."""
        total = len(self.students_list)
        if total == 0:
            return {
                "total": 0,
                "promedio_general": 0.0,
                "mejor_estudiante": None,
                "menor_estudiante": None,
            }

        suma_promedios = 0.0
        mejor: Optional[Estudiante] = None
        menor: Optional[Estudiante] = None

        for est in self.students_list:
            prom = est.calcular_promedio()
            suma_promedios += prom
            if mejor is None or prom > mejor.calcular_promedio():
                mejor = est
            if menor is None or prom < menor.calcular_promedio():
                menor = est

        return {
            "total": total,
            "promedio_general": round(suma_promedios / total, 2),
            "mejor_estudiante": mejor,
            "menor_estudiante": menor,
        }

    def get_doubly_linked_nodes_data(self) -> List[Dict[str, Any]]:
        """Extrae la información de cada nodo con sus referencias prev y next
        para renderizar flechas y tarjetas en la vista gráfica.
        """
        nodes_info: List[Dict[str, Any]] = []
        current = self.students_list.head
        index = 0
        total = len(self.students_list)

        while current:
            est: Estudiante = current.data
            prev_id = current.prev.data.id if current.prev else None
            next_id = current.next.data.id if current.next else None

            nodes_info.append({
                "index": index,
                "id": est.id,
                "nombre": est.nombre,
                "apellido": est.apellido,
                "promedio": est.calcular_promedio(),
                "notas": est.calificaciones.to_list(),
                "prev_id": prev_id,
                "next_id": next_id,
                "is_head": current == self.students_list.head,
                "is_tail": current == self.students_list.tail,
            })
            current = current.next
            index += 1

        return nodes_info

    def get_undo_stack_items(self) -> List[str]:
        """Obtiene la lista de descripciones en la pila de deshacer (de la cima a la base)."""
        items: List[str] = []
        for action in self.undo_manager.undo_stack:
            items.append(action.description or action.action_type)
        return items

    def get_redo_stack_items(self) -> List[str]:
        """Obtiene la lista de descripciones en la pila de rehacer (de la cima a la base)."""
        items: List[str] = []
        for action in self.undo_manager.redo_stack:
            items.append(action.description or action.action_type)
        return items

    def get_priority_queue_items(self) -> List[Dict[str, Any]]:
        """Obtiene las solicitudes en la cola de prioridad ordenadas por urgencia."""
        items: List[Dict[str, Any]] = []
        for data, priority in self.priority_admissions:
            items.append({
                "estudiante": data,
                "prioridad": priority,
            })
        return items

    def get_circular_nodes_data(self) -> List[Dict[str, Any]]:
        """Obtiene los nodos de la Lista/Cola Circular con sus punteros bidireccionales."""
        items: List[Dict[str, Any]] = []
        if self.review_round.is_empty():
            return items
        current = self.review_round.head
        for idx in range(len(self.review_round)):
            if not current:
                break
            est: Estudiante = current.data
            items.append({
                "index": idx,
                "id": est.id,
                "nombre": est.nombre,
                "apellido": est.apellido,
                "promedio": est.calcular_promedio(),
                "prev_id": current.prev.data.id if current.prev else None,
                "next_id": current.next.data.id if current.next else None,
                "is_current": current == self.review_round.head,
            })
            current = current.next
        return items

