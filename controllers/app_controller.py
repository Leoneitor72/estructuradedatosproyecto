"""Controlador Principal de la Aplicación (Patrón MVC).
Mediación entre eventos de usuario en la UI y operaciones del Modelo.
Aislamiento estricto: La vista solo interactúa con el Modelo a través de este controlador.
"""

from typing import Optional, List, Dict, Any, Callable
from models.student_engine import StudentEngine
from models.student import Estudiante


class AppController:
    """Controlador mediador que conecta la interfaz gráfica Flet con el motor de estructuras."""

    def __init__(self, engine: Optional[StudentEngine] = None):
        self.model: StudentEngine = engine if engine is not None else StudentEngine(sort_by="apellido")
        self._on_state_changed_callbacks: List[Callable[[], None]] = []

    def register_listener(self, callback: Callable[[], None]) -> None:
        """Permite a la vista registrar una función de refresco automático ante cambios de estado."""
        if callback not in self._on_state_changed_callbacks:
            self._on_state_changed_callbacks.append(callback)

    def _notify_state_changed(self) -> None:
        """Notifica a todos los escuchas registrados que el modelo cambió."""
        for cb in self._on_state_changed_callbacks:
            try:
                cb()
            except Exception:
                pass

    # =========================================================================
    # EVENTOS DE NEGOCIO (ESTUDIANTES)
    # =========================================================================

    def inscribir_estudiante(
        self,
        id_estudiante: str,
        nombre: str,
        apellido: str,
        notas_raw: str = "",
        sort_by: Optional[str] = "apellido",
    ) -> Dict[str, Any]:
        """Procesa el evento de inscripción de un estudiante desde el formulario de la UI."""
        id_clean = id_estudiante.strip().upper()
        nombre_clean = nombre.strip().title()
        apellido_clean = apellido.strip().title()

        if not id_clean or not nombre_clean or not apellido_clean:
            return {"success": False, "message": "ID, Nombre y Apellido son obligatorios."}

        # Parsear notas opcionales
        notas_list: List[float] = []
        if notas_raw.strip():
            partes = [p.strip() for p in notas_raw.replace(";", ",").split(",") if p.strip()]
            for p in partes:
                try:
                    val = float(p)
                    if 0.0 <= val <= 20.0 or 0.0 <= val <= 100.0:
                        notas_list.append(val)
                    else:
                        return {"success": False, "message": f"Calificación fuera de rango: {val}"}
                except ValueError:
                    return {"success": False, "message": f"Formato de nota inválido: '{p}'"}

        try:
            self.model.set_sort_mode(sort_by)
            est = self.model.inscribir_estudiante(id_clean, nombre_clean, apellido_clean, notas_list)
            self._notify_state_changed()
            return {
                "success": True,
                "message": f"Estudiante {est.nombre} {est.apellido} ({est.id}) inscrito con éxito.",
                "data": est.to_dict(),
            }
        except ValueError as e:
            return {"success": False, "message": str(e)}

    def dar_de_baja(self, id_estudiante: str) -> Dict[str, Any]:
        """Procesa la eliminación de un estudiante por su ID."""
        id_clean = id_estudiante.strip().upper()
        if not id_clean:
            return {"success": False, "message": "Debe especificar un ID válido."}

        eliminado = self.model.dar_de_baja(id_clean)
        if eliminado:
            self._notify_state_changed()
            return {"success": True, "message": f"Estudiante con ID {id_clean} dado de baja."}
        else:
            return {"success": False, "message": f"No se encontró ningún estudiante con el ID: {id_clean}"}

    def actualizar_calificaciones(self, id_estudiante: str, notas_raw: str) -> Dict[str, Any]:
        """Procesa la actualización de calificaciones."""
        id_clean = id_estudiante.strip().upper()
        if not id_clean:
            return {"success": False, "message": "Debe especificar un ID de estudiante."}

        partes = [p.strip() for p in notas_raw.replace(";", ",").split(",") if p.strip()]
        if not partes:
            return {"success": False, "message": "Debe ingresar al menos una calificación."}

        nuevas_notas: List[float] = []
        for p in partes:
            try:
                nuevas_notas.append(float(p))
            except ValueError:
                return {"success": False, "message": f"Calificación no válida: '{p}'"}

        actualizado = self.model.actualizar_calificaciones(id_clean, nuevas_notas)
        if actualizado:
            promedio = self.model.calcular_promedio(id_clean)
            self._notify_state_changed()
            return {
                "success": True,
                "message": f"Notas de {id_clean} actualizadas. Nuevo promedio: {promedio:.2f}",
            }
        else:
            return {"success": False, "message": f"No se encontró al estudiante con ID: {id_clean}"}

    def buscar_estudiante(self, id_estudiante: str) -> Optional[Dict[str, Any]]:
        """Busca un estudiante y retorna sus datos serializados para la vista."""
        id_clean = id_estudiante.strip().upper()
        est = self.model.buscar_estudiante(id_clean)
        return est.to_dict() if est else None

    # =========================================================================
    # EVENTOS DE DESHACER Y REHACER (UNDO / REDO)
    # =========================================================================

    def deshacer(self) -> Dict[str, Any]:
        """Revierte la última acción en la pila."""
        if not self.model.undo_manager.can_undo():
            return {"success": False, "message": "No hay acciones para deshacer."}

        msg = self.model.deshacer()
        self._notify_state_changed()
        return {"success": True, "message": msg or "Acción revertida."}

    def rehacer(self) -> Dict[str, Any]:
        """Reaplica la última acción revertida."""
        if not self.model.undo_manager.can_redo():
            return {"success": False, "message": "No hay acciones para rehacer."}

        msg = self.model.rehacer()
        self._notify_state_changed()
        return {"success": True, "message": msg or "Acción repetida."}

    # =========================================================================
    # EVENTOS DE COLAS (PRIORIDAD Y CIRCULAR)
    # =========================================================================

    def encolar_admision_prioritaria(
        self, id_sol: str, nombre: str, apellido: str, prioridad: float
    ) -> Dict[str, Any]:
        """Encola un postulante en la cola de prioridad."""
        est = Estudiante(id_sol.strip().upper(), nombre.strip(), apellido.strip())
        self.model.encolar_solicitud_prioritaria(est, prioridad)
        self._notify_state_changed()
        return {
            "success": True,
            "message": f"Solicitud de {nombre} {apellido} encolada con prioridad {prioridad:.1f}.",
        }

    def atender_siguiente_prioridad(self) -> Dict[str, Any]:
        """Atiende la solicitud con mayor prioridad en O(1)."""
        est = self.model.atender_siguiente_solicitud()
        if not est:
            return {"success": False, "message": "No hay solicitudes pendientes en la cola."}

        self._notify_state_changed()
        return {
            "success": True,
            "message": f"Solicitud atendida: {est.nombre} {est.apellido} ({est.id}).",
            "data": est.to_dict(),
        }

    def avanzar_turno_circular(self) -> Dict[str, Any]:
        """Avanza el turno circular de revisión de estudiantes en O(1)."""
        if self.model.review_round.is_empty():
            self.model.cargar_ronda_circular()

        est = self.model.siguiente_en_turno()
        if not est:
            return {"success": False, "message": "No hay estudiantes en la ronda circular."}

        self._notify_state_changed()
        return {
            "success": True,
            "message": f"Turno actual: {est.nombre} {est.apellido} ({est.id}) - Promedio: {est.calcular_promedio():.2f}",
            "data": est.to_dict(),
        }

    def retroceder_turno_circular(self) -> Dict[str, Any]:
        """Retrocede el turno en la ruta circular bidireccional en O(1)."""
        if self.model.review_round.is_empty():
            self.model.cargar_ronda_circular()

        est = self.model.anterior_en_turno()
        if not est:
            return {"success": False, "message": "No hay estudiantes en la ronda circular."}

        self._notify_state_changed()
        return {
            "success": True,
            "message": f"Turno anterior: {est.nombre} {est.apellido} ({est.id}) - Promedio: {est.calcular_promedio():.2f}",
            "data": est.to_dict(),
        }

    # =========================================================================
    # CONSULTAS DE ESTADO PARA LAS VISTAS GRÁFICAS (DÍA 3)
    # =========================================================================

    def get_doubly_linked_list_nodes(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de nodos con referencias prev y next para el visualizador."""
        return self.model.get_doubly_linked_nodes_data()

    def get_circular_list_nodes(self) -> List[Dict[str, Any]]:
        """Obtiene los nodos de la Lista/Cola Circular para el circuito animado."""
        return self.model.get_circular_nodes_data()

    def get_undo_stack_items(self) -> List[str]:
        return self.model.get_undo_stack_items()

    def get_redo_stack_items(self) -> List[str]:
        return self.model.get_redo_stack_items()

    def get_priority_queue_items(self) -> List[Dict[str, Any]]:
        return self.model.get_priority_queue_items()

    def get_students_table(self) -> List[Dict[str, Any]]:
        return self.model.generar_reporte()

    def get_statistics(self) -> Dict[str, Any]:
        return self.model.get_statistics()

    def can_undo(self) -> bool:
        return self.model.undo_manager.can_undo()

    def can_redo(self) -> bool:
        return self.model.undo_manager.can_redo()

    def run_benchmarks(self, iterations: int = 3000) -> Dict[str, Any]:
        """Ejecuta suite de rendimiento y memoria en tiempo real."""
        from models.benchmarks import run_benchmark_suite, get_memory_footprint
        return {
            "benchmarks": run_benchmark_suite(iterations),
            "memory": get_memory_footprint(),
        }

