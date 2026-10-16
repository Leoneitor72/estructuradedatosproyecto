"""Motor lógico del Sistema de Gestión de Estudiantes.
Orquesta las estructuras de datos puras (DoublyLinkedList, Stack/UndoRedoManager, PriorityQueue, CircularQueue)
con la lógica de negocio requerida.
"""

from typing import Optional, List, Dict, Any, Iterable, Union
from .structures import DoublyLinkedList, PriorityQueue, CircularQueue
from .student import Estudiante
from .undo_redo import UndoRedoManager, Action


class StudentManager:
    """Gestor principal de estudiantes implementado con estructuras de datos manuales."""

    def __init__(self, sort_by: Optional[str] = None):
        """Inicializa el gestor.
        :param sort_by: None para inserción al final (append), 'id' para ordenar por ID, 'apellido' para ordenar por apellido.
        """
        self.students_list: DoublyLinkedList = DoublyLinkedList()
        self.undo_manager: UndoRedoManager = UndoRedoManager()
        self.priority_admissions: PriorityQueue = PriorityQueue()
        self.review_round: CircularQueue = CircularQueue()
        self.sort_by: Optional[str] = sort_by

    def set_sort_mode(self, sort_by: Optional[str]) -> None:
        """Modifica el criterio de ordenamiento ('id', 'apellido' o None)."""
        self.sort_by = sort_by

    def inscribir_estudiante(
        self,
        id_estudiante: str,
        nombre: str,
        apellido: str,
        calificaciones: Optional[Iterable[Union[int, float]]] = None,
        record_history: bool = True,
    ) -> Estudiante:
        """Funcionalidad 1: Inscribir Estudiante.
        Añade un nuevo estudiante a la lista (al final o de forma ordenada por ID/apellido).
        Lanza ValueError si el ID ya existe.
        """
        id_clean = str(id_estudiante).strip()
        if self.buscar_estudiante(id_clean) is not None:
            raise ValueError(f"Ya existe un estudiante con el ID: {id_clean}")

        estudiante = Estudiante(id_clean, nombre, apellido, calificaciones)

        if self.sort_by == "id":
            self.students_list.insert_ordered(estudiante, key_func=lambda est: est.id)
        elif self.sort_by == "apellido":
            self.students_list.insert_ordered(estudiante, key_func=lambda est: (est.apellido.lower(), est.nombre.lower()))
        else:
            self.students_list.append(estudiante)

        # Sincronizar ronda circular
        self.review_round.enqueue(estudiante)

        if record_history:
            self.undo_manager.record_action(
                Action(
                    action_type=Action.ADD,
                    payload={"estudiante": estudiante},
                    description=f"Inscripción de estudiante {estudiante.id} - {estudiante.nombre} {estudiante.apellido}",
                )
            )

        return estudiante


    def dar_de_baja(self, id_estudiante: str, record_history: bool = True) -> bool:
        """Funcionalidad 2: Dar de Baja a Estudiante.
        Elimina a un estudiante de la lista por su ID.
        Retorna True si fue eliminado, False si no se encontró.
        """
        id_clean = str(id_estudiante).strip()
        estudiante = self.buscar_estudiante(id_clean)
        if not estudiante:
            return False

        # Guardar notas para posible undo
        notas_actuales = estudiante.calificaciones.to_list()

        eliminado = self.students_list.remove(lambda est: est.id == id_clean)
        if eliminado:
            self.cargar_ronda_circular()
            if record_history:
                self.undo_manager.record_action(
                    Action(
                        action_type=Action.REMOVE,
                        payload={
                            "id": estudiante.id,
                            "nombre": estudiante.nombre,
                            "apellido": estudiante.apellido,
                            "calificaciones": notas_actuales,
                        },
                        description=f"Baja de estudiante {estudiante.id} ({estudiante.apellido})",
                    )
                )
        return eliminado


    def buscar_estudiante(self, id_estudiante: str) -> Optional[Estudiante]:
        """Busca un estudiante en la lista enlazada por su ID O(n)."""
        id_clean = str(id_estudiante).strip()
        return self.students_list.search(lambda est: est.id == id_clean)

    def actualizar_calificaciones(
        self,
        id_estudiante: str,
        nuevas_calificaciones: Iterable[Union[int, float]],
        record_history: bool = True,
    ) -> bool:
        """Funcionalidad 3: Actualizar Calificaciones.
        Busca un estudiante y modifica sus notas.
        Retorna True si se actualizó, False si no fue encontrado.
        """
        estudiante = self.buscar_estudiante(id_estudiante)
        if not estudiante:
            return False

        calificaciones_previas = estudiante.calificaciones.to_list()
        nuevas_lista = [float(n) for n in nuevas_calificaciones]
        estudiante.actualizar_calificaciones(nuevas_lista)

        if record_history:
            self.undo_manager.record_action(
                Action(
                    action_type=Action.UPDATE_GRADES,
                    payload={
                        "id": estudiante.id,
                        "old_grades": calificaciones_previas,
                        "new_grades": nuevas_lista,
                    },
                    description=f"Actualización de notas para estudiante {estudiante.id}",
                )
            )
        return True

    def calcular_promedio(self, id_estudiante: str) -> Optional[float]:
        """Funcionalidad 4: Calcular Promedio.
        Busca un estudiante y calcula el promedio de sus calificaciones.
        Retorna None si no existe.
        """
        estudiante = self.buscar_estudiante(id_estudiante)
        if not estudiante:
            return None
        return estudiante.calcular_promedio()

    def generar_reporte(self) -> List[Dict[str, Any]]:
        """Funcionalidad 5: Generar Reporte.
        Retorna una lista con la información completa de todos los estudiantes inscritos.
        """
        reporte: List[Dict[str, Any]] = []
        for estudiante in self.students_list:
            reporte.append(estudiante.to_dict())
        return reporte

    def generar_reporte_texto(self) -> str:
        """Genera una versión en texto formateado del reporte de estudiantes."""
        if self.students_list.is_empty():
            return "No hay estudiantes inscritos en el sistema."

        lineas = [
            "=" * 70,
            f"{'ID':<10} | {'APELLIDO':<15} | {'NOMBRE':<15} | {'PROMEDIO':<8} | NOTAS",
            "-" * 70,
        ]
        for est in self.students_list:
            notas_str = ", ".join(f"{g:.1f}" for g in est.calificaciones) or "Sin notas"
            lineas.append(
                f"{est.id:<10} | {est.apellido:<15} | {est.nombre:<15} | {est.calcular_promedio():<8.2f} | {notas_str}"
            )
        lineas.append("=" * 70)
        lineas.append(f"Total inscritos: {len(self.students_list)}")
        return "\n".join(lineas)

    # --- Gestión Undo / Redo mediante Pila ---
    def deshacer(self) -> Optional[str]:
        """Revierte la última acción registrada."""
        action = self.undo_manager.undo()
        if not action:
            return None

        if action.action_type == Action.ADD:
            est = action.payload["estudiante"]
            self.students_list.remove(lambda e: e.id == est.id)
            return f"Deshecho: Se removio al estudiante inscrito ({est.id})"

        elif action.action_type == Action.REMOVE:
            p = action.payload
            est_restaurado = Estudiante(p["id"], p["nombre"], p["apellido"], p["calificaciones"])
            if self.sort_by == "id":
                self.students_list.insert_ordered(est_restaurado, key_func=lambda e: e.id)
            elif self.sort_by == "apellido":
                self.students_list.insert_ordered(est_restaurado, key_func=lambda e: (e.apellido.lower(), e.nombre.lower()))
            else:
                self.students_list.append(est_restaurado)
            return f"Deshecho: Se restauro al estudiante dado de baja ({p['id']})"

        elif action.action_type == Action.UPDATE_GRADES:
            p = action.payload
            est = self.buscar_estudiante(p["id"])
            if est:
                est.actualizar_calificaciones(p["old_grades"])
            return f"Deshecho: Se restauraron las calificaciones anteriores de ({p['id']})"

        return None

    def rehacer(self) -> Optional[str]:
        """Aplica nuevamente la última acción revertida."""
        action = self.undo_manager.redo()
        if not action:
            return None

        if action.action_type == Action.ADD:
            est = action.payload["estudiante"]
            if self.sort_by == "id":
                self.students_list.insert_ordered(est, key_func=lambda e: e.id)
            elif self.sort_by == "apellido":
                self.students_list.insert_ordered(est, key_func=lambda e: (e.apellido.lower(), e.nombre.lower()))
            else:
                self.students_list.append(est)
            return f"Rehecho: Se volvio a inscribir al estudiante ({est.id})"

        elif action.action_type == Action.REMOVE:
            p = action.payload
            self.students_list.remove(lambda e: e.id == p["id"])
            return f"Rehecho: Se volvio a dar de baja al estudiante ({p['id']})"

        elif action.action_type == Action.UPDATE_GRADES:
            p = action.payload
            est = self.buscar_estudiante(p["id"])
            if est:
                est.actualizar_calificaciones(p["new_grades"])
            return f"Rehecho: Se volvieron a aplicar las calificaciones nuevas de ({p['id']})"

        return None

    # --- Cola de Prioridad para Admisiones / Solicitudes ---
    def encolar_solicitud_prioritaria(self, estudiante: Estudiante, prioridad: float) -> None:
        """Encola una solicitud en la cola de prioridad O(n)."""
        self.priority_admissions.enqueue(estudiante, prioridad)

    def atender_siguiente_solicitud(self) -> Optional[Estudiante]:
        """Extrae y atiende la solicitud de mayor prioridad O(1)."""
        return self.priority_admissions.dequeue()

    # --- Cola Circular para Rondas de Evaluación / Turnos ---
    def cargar_ronda_circular(self) -> None:
        """Carga a todos los estudiantes actuales en la cola circular de turnos."""
        self.review_round.clear()
        for est in self.students_list:
            self.review_round.enqueue(est)

    def siguiente_en_turno(self) -> Optional[Estudiante]:
        """Avanza al siguiente estudiante en el turno circular Round-Robin O(1)."""
        return self.review_round.step()

    def anterior_en_turno(self) -> Optional[Estudiante]:
        """Retrocede al estudiante previo en la ruta circular bidireccional O(1)."""
        return self.review_round.step_backward()

