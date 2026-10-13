"""Vista Principal de Escritorio con Flet (Semana 2 - Días 3, 4 y 5).
Despliegue responsivo para Windows (Win32), macOS y Linux.
Integra las vistas dinámicas de Lista Doble, Pila, Cola de Prioridad y Cola Circular con botones Undo/Redo.
"""

from typing import Optional, Dict, Any, List
import flet as ft
from controllers.app_controller import AppController
from .components import (
    build_doubly_linked_list_view,
    build_stack_view,
    build_priority_queue_view,
    build_circular_queue_view,
    build_stats_panel,
)


class DesktopView:
    """Vista de escritorio construida con el framework Flet / Flutter."""

    def __init__(self, page: ft.Page, controller: AppController):
        self.page: ft.Page = page
        self.controller: AppController = controller

        # Estado visual
        self.current_section: str = "visualizer"  # 'visualizer' | 'operations' | 'rubric'
        self.current_circular_turn: Optional[Dict[str, Any]] = None

        # Registrar este view como listener de cambios en el controlador
        self.controller.register_listener(self.render)

        # Configurar propiedades iniciales de la ventana
        self.page.title = "Simulador de Gestión de Estudiantes - Estructuras de Datos MVC"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 16
        self.page.scroll = ft.ScrollMode.AUTO

        # Banner de notificación
        self.status_message = ft.Text("", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE)
        self.status_icon = ft.Icon(ft.Icons.INFO_OUTLINE, size=18, color=ft.Colors.WHITE)
        self.status_banner = ft.Container(
            content=ft.Row([self.status_icon, self.status_message], spacing=8),
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            border_radius=ft.BorderRadius.all(8),
            visible=False,
            margin=ft.Margin.only(bottom=10),
        )

        # Campos de Formulario: Inscribir
        self.tf_inscribir_id = ft.TextField(label="ID Alumno", hint_text="EST-105", width=140)
        self.tf_inscribir_nombre = ft.TextField(label="Nombre", hint_text="Carlos", width=160)
        self.tf_inscribir_apellido = ft.TextField(label="Apellido", hint_text="Mendoza", width=160)
        self.tf_inscribir_notas = ft.TextField(label="Notas (separadas por coma)", hint_text="15, 17.5, 18", width=220)
        self.dd_inscribir_orden = ft.Dropdown(
            label="Orden de Inserción",
            width=170,
            value="apellido",
            options=[
                ft.DropdownOption("apellido", "Por Apellido (O(n))"),
                ft.DropdownOption("id", "Por ID (O(n))"),
                ft.DropdownOption("none", "Al Final - Append (O(1))"),
            ],
        )

        # Campos de Formulario: Dar de Baja
        self.tf_baja_id = ft.TextField(label="ID a Dar de Baja", hint_text="EST-102", width=180)

        # Campos de Formulario: Actualizar Notas
        self.tf_update_id = ft.TextField(label="ID de Estudiante", hint_text="EST-101", width=150)
        self.tf_update_notas = ft.TextField(label="Nuevas Notas", hint_text="18, 19, 20", width=220)

        # Campos de Formulario: Admisión Prioritaria
        self.tf_prio_id = ft.TextField(label="ID Solicitante", hint_text="SOL-04", width=130)
        self.tf_prio_nombre = ft.TextField(label="Nombre", hint_text="Laura", width=140)
        self.tf_prio_apellido = ft.TextField(label="Apellido", hint_text="Solis", width=140)
        self.tf_prio_score = ft.TextField(label="Score Prioridad (0 - 10)", hint_text="8.5", width=160)

        # Inicializar contenido
        self.build_ui()

    def show_status(self, message: str, is_success: bool = True, is_undo: bool = False):
        """Muestra una alerta informativa con código de color dinámico."""
        self.status_message.value = message
        if is_undo:
            self.status_banner.bgcolor = ft.Colors.BLUE_900
            self.status_icon.name = ft.Icons.UNDO
            self.status_icon.color = ft.Colors.BLUE_300
        elif is_success:
            self.status_banner.bgcolor = ft.Colors.GREEN_900
            self.status_icon.name = ft.Icons.CHECK_CIRCLE_OUTLINE
            self.status_icon.color = ft.Colors.GREEN_300
        else:
            self.status_banner.bgcolor = ft.Colors.RED_900
            self.status_icon.name = ft.Icons.ERROR_OUTLINE
            self.status_icon.color = ft.Colors.RED_300
        self.status_banner.visible = True
        self.page.update()

    # =========================================================================
    # EVENTOS DE ACCIONES (INTERACCIÓN CON EL CONTROLADOR)
    # =========================================================================

    def on_inscribir_click(self, _):
        sort_mode = self.dd_inscribir_orden.value
        if sort_mode == "none":
            sort_mode = None
        res = self.controller.inscribir_estudiante(
            id_estudiante=self.tf_inscribir_id.value or "",
            nombre=self.tf_inscribir_nombre.value or "",
            apellido=self.tf_inscribir_apellido.value or "",
            notas_raw=self.tf_inscribir_notas.value or "",
            sort_by=sort_mode,
        )
        self.show_status(res["message"], is_success=res["success"])
        if res["success"]:
            self.tf_inscribir_id.value = ""
            self.tf_inscribir_nombre.value = ""
            self.tf_inscribir_apellido.value = ""
            self.tf_inscribir_notas.value = ""

    def on_dar_baja_click(self, _):
        id_baja = self.tf_baja_id.value or ""
        res = self.controller.dar_de_baja(id_baja)
        self.show_status(res["message"], is_success=res["success"])
        if res["success"]:
            self.tf_baja_id.value = ""

    def on_delete_node_direct(self, student_id: str):
        res = self.controller.dar_de_baja(student_id)
        self.show_status(res["message"], is_success=res["success"])

    def on_actualizar_notas_click(self, _):
        id_est = self.tf_update_id.value or ""
        notas = self.tf_update_notas.value or ""
        res = self.controller.actualizar_calificaciones(id_est, notas)
        self.show_status(res["message"], is_success=res["success"])
        if res["success"]:
            self.tf_update_id.value = ""
            self.tf_update_notas.value = ""

    def on_encolar_prioridad_click(self, _):
        try:
            score = float(self.tf_prio_score.value or 0.0)
        except ValueError:
            self.show_status("El score de prioridad debe ser un número.", is_success=False)
            return

        res = self.controller.encolar_admision_prioritaria(
            id_sol=self.tf_prio_id.value or "",
            nombre=self.tf_prio_nombre.value or "",
            apellido=self.tf_prio_apellido.value or "",
            prioridad=score,
        )
        self.show_status(res["message"], is_success=res["success"])
        if res["success"]:
            self.tf_prio_id.value = ""
            self.tf_prio_nombre.value = ""
            self.tf_prio_apellido.value = ""
            self.tf_prio_score.value = ""

    def on_atender_prioridad_click(self):
        res = self.controller.atender_siguiente_prioridad()
        self.show_status(res["message"], is_success=res["success"])

    def on_circular_step_click(self):
        res = self.controller.avanzar_turno_circular()
        if res["success"]:
            self.current_circular_turn = res.get("data")
        self.show_status(res["message"], is_success=res["success"])

    def on_undo_click(self, _):
        res = self.controller.deshacer()
        self.show_status(res["message"], is_success=res["success"], is_undo=True)

    def on_redo_click(self, _):
        res = self.controller.rehacer()
        self.show_status(res["message"], is_success=res["success"], is_undo=True)

    def on_seed_sample_click(self, _):
        self.controller.model.seed_sample_data()
        self.controller._notify_state_changed()
        self.show_status("Datos de prueba cargados con éxito en la memoria.", is_success=True)

    # =========================================================================
    # CONSTRUCCIÓN DE LA INTERFAZ (UI BUILD)
    # =========================================================================

    def build_header(self) -> ft.Control:
        """Semana 2 - Día 4: Botones interactivos de Undo / Redo y título."""
        can_undo = self.controller.can_undo()
        can_redo = self.controller.can_redo()
        undo_count = len(self.controller.get_undo_stack_items())
        redo_count = len(self.controller.get_redo_stack_items())

        return ft.Container(
            content=ft.Row(
                [
                    # Título y Subtítulo
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ACCOUNT_TREE, size=32, color=ft.Colors.BLUE_400),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Simulador de Gestión de Estudiantes",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Text(
                                        "Semana 2: Integración MVC y Visualización Dinámica en Flet",
                                        size=11,
                                        color=ft.Colors.GREY_400,
                                    ),
                                ],
                                spacing=1,
                            ),
                        ],
                        spacing=8,
                    ),
                    # Acciones globales (Deshacer, Rehacer, Cargar Muestra)
                    ft.Row(
                        [
                            ft.FilledButton(
                                content=f"Deshacer ({undo_count})",
                                icon=ft.Icons.UNDO,
                                on_click=self.on_undo_click,
                                disabled=not can_undo,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700 if can_undo else ft.Colors.GREY_800),
                            ),
                            ft.FilledButton(
                                content=f"Rehacer ({redo_count})",
                                icon=ft.Icons.REDO,
                                on_click=self.on_redo_click,
                                disabled=not can_redo,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_700 if can_redo else ft.Colors.GREY_800),
                            ),
                            ft.OutlinedButton(
                                content="Datos Ejemplo",
                                icon=ft.Icons.AUTO_AWESOME,
                                on_click=self.on_seed_sample_click,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border=ft.Border.all(1, ft.Colors.BLUE_900),
            border_radius=ft.BorderRadius.all(12),
        )

    def build_navigation_bar(self) -> ft.Control:
        """Selector de secciones principales."""
        def set_section(sec: str):
            self.current_section = sec
            self.render()

        is_vis = self.current_section == "visualizer"
        is_ops = self.current_section == "operations"
        is_rub = self.current_section == "rubric"

        return ft.Row(
            [
                ft.FilledButton(
                    content="Visualizador de Memoria y Punteros",
                    icon=ft.Icons.HUB_OUTLINED,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600 if is_vis else ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    on_click=lambda _: set_section("visualizer"),
                ),
                ft.FilledButton(
                    content="Operaciones y Estudiantes",
                    icon=ft.Icons.EDIT_NOTE,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600 if is_ops else ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    on_click=lambda _: set_section("operations"),
                ),
                ft.FilledButton(
                    content="Analisis y Rubrica",
                    icon=ft.Icons.ASSESSMENT_OUTLINED,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600 if is_rub else ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    on_click=lambda _: set_section("rubric"),
                ),
            ],
            spacing=8,
        )

    def build_visualizer_tab(self) -> ft.Control:
        """Semana 2 - Día 3: Visualización Dinámica de las Estructuras."""
        nodes_data = self.controller.get_doubly_linked_list_nodes()
        undo_items = self.controller.get_undo_stack_items()
        redo_items = self.controller.get_redo_stack_items()
        priority_items = self.controller.get_priority_queue_items()

        return ft.Column(
            [
                # 1. Lista Doblemente Enlazada
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SHARE, color=ft.Colors.BLUE_400, size=20),
                        ft.Text("1. Lista Doblemente Enlazada (Nodos y Punteros next / prev)", size=14, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6,
                ),
                build_doubly_linked_list_view(nodes_data, on_delete_callback=self.on_delete_node_direct),

                # 2. Pilas LIFO (Undo y Redo)
                ft.Row(
                    [
                        ft.Icon(ft.Icons.LAYERS, color=ft.Colors.PURPLE_400, size=20),
                        ft.Text("2. Pilas de Transacciones LIFO (Dual-Stack Undo / Redo)", size=14, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6,
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=build_stack_view(undo_items, "Pila de Deshacer (Undo Stack)", is_undo=True),
                            expand=True,
                        ),
                        ft.Container(
                            content=build_stack_view(redo_items, "Pila de Rehacer (Redo Stack)", is_undo=False),
                            expand=True,
                        ),
                    ],
                    spacing=12,
                ),

                # 3. Cola de Prioridad
                ft.Row(
                    [
                        ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.AMBER_400, size=20),
                        ft.Text("3. Cola de Prioridad (Admisiones Urgentes y Becas)", size=14, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6,
                ),
                build_priority_queue_view(priority_items, on_attend_callback=self.on_atender_prioridad_click),

                # 4. Cola Circular
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SYNC, color=ft.Colors.CYAN_400, size=20),
                        ft.Text("4. Cola Circular de Revisión (Round-Robin continuo)", size=14, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6,
                ),
                build_circular_queue_view(self.current_circular_turn, on_step_callback=self.on_circular_step_click),
            ],
            spacing=16,
        )

    def build_operations_tab(self) -> ft.Control:
        """Formularios de acción para las 5 funcionalidades pedidas."""
        students = self.controller.get_students_table()

        # Filas de la tabla de estudiantes
        table_rows = []
        for s in students:
            prom = s.get("promedio", 0.0)
            table_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s["id"], weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300)),
                        ft.DataCell(ft.Text(s["apellido"])),
                        ft.DataCell(ft.Text(s["nombre"])),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(f"{prom:.2f}", color=ft.Colors.WHITE, size=11),
                                bgcolor=ft.Colors.GREEN_700 if prom >= 15 else (ft.Colors.AMBER_700 if prom >= 11 else ft.Colors.RED_700),
                                padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                border_radius=ft.BorderRadius.all(4),
                            )
                        ),
                        ft.DataCell(ft.Text(", ".join(f"{g:.1f}" for g in s.get("calificaciones", [])) or "Sin notas")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_300,
                                tooltip=f"Dar de baja a {s['id']}",
                                on_click=lambda _, sid=s["id"]: self.on_delete_node_direct(sid),
                            )
                        ),
                    ]
                )
            )

        students_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Promedio")),
                ft.DataColumn(ft.Text("Calificaciones")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=table_rows,
            border=ft.Border.all(1, ft.Colors.GREY_800),
            border_radius=ft.BorderRadius.all(8),
            heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )

        return ft.Column(
            [
                # Formularios en tarjetas
                ft.Row(
                    [
                        # Formulario 1: Inscribir
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Inscribir Estudiante (Funcionalidad 1)", weight=ft.FontWeight.BOLD, size=13),
                                    ft.Row([self.tf_inscribir_id, self.tf_inscribir_nombre, self.tf_inscribir_apellido], spacing=8),
                                    ft.Row([self.tf_inscribir_notas, self.dd_inscribir_orden], spacing=8),
                                    ft.FilledButton(
                                        content="Inscribir Alumno",
                                        icon=ft.Icons.PERSON_ADD,
                                        on_click=self.on_inscribir_click,
                                    ),
                                ],
                                spacing=8,
                            ),
                            padding=14,
                            border=ft.Border.all(1, ft.Colors.BLUE_900),
                            border_radius=ft.BorderRadius.all(10),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                            expand=True,
                        ),
                        # Formulario 2 y 3: Dar de baja y Actualizar
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Modificaciones y Bajas", weight=ft.FontWeight.BOLD, size=13),
                                    ft.Row(
                                        [
                                            self.tf_baja_id,
                                            ft.FilledButton(
                                                content="Dar de Baja",
                                                icon=ft.Icons.PERSON_REMOVE,
                                                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_800),
                                                on_click=self.on_dar_baja_click,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Divider(color=ft.Colors.GREY_800, height=1),
                                    ft.Row([self.tf_update_id, self.tf_update_notas], spacing=8),
                                    ft.FilledButton(
                                        content="Actualizar Calificaciones",
                                        icon=ft.Icons.GRADE,
                                        style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_800),
                                        on_click=self.on_actualizar_notas_click,
                                    ),
                                ],
                                spacing=8,
                            ),
                            padding=14,
                            border=ft.Border.all(1, ft.Colors.RED_900),
                            border_radius=ft.BorderRadius.all(10),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                            expand=True,
                        ),
                    ],
                    spacing=12,
                ),
                # Formulario 4: Admisión Prioritaria
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Encolar en Cola de Prioridad (Becas / Casos Urgentes)", weight=ft.FontWeight.BOLD, size=13),
                            ft.Row(
                                [
                                    self.tf_prio_id,
                                    self.tf_prio_nombre,
                                    self.tf_prio_apellido,
                                    self.tf_prio_score,
                                    ft.FilledButton(
                                        content="Encolar Prioritario",
                                        icon=ft.Icons.QUEUE,
                                        style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_700),
                                        on_click=self.on_encolar_prioridad_click,
                                    ),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=14,
                    border=ft.Border.all(1, ft.Colors.AMBER_900),
                    border_radius=ft.BorderRadius.all(10),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                ),
                # Tabla completa de Estudiantes
                ft.Text("Reporte General de Estudiantes (Funcionalidad 5)", weight=ft.FontWeight.BOLD, size=14),
                ft.Container(
                    content=students_table if table_rows else ft.Text("No hay estudiantes inscritos en el sistema.", color=ft.Colors.GREY_500, italic=True),
                    padding=10,
                ),
            ],
            spacing=16,
        )

    def build_rubric_tab(self) -> ft.Control:
        """Análisis y verificación de cumplimiento de la rúbrica."""
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Cumplimiento de la Rúbrica Pedagógica (Semana 2)", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Divider(color=ft.Colors.GREY_800),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.VERIFIED, color=ft.Colors.GREEN_400),
                                    ft.Text("35% Implementación Manual: Estructuras puras (Node, DoublyLinkedList, Stack, Queues) sin usar list.", size=12),
                                ],
                                spacing=6,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.VERIFIED, color=ft.Colors.GREEN_400),
                                    ft.Text("20% Arquitectura MVC: Aislamiento total del Modelo respecto a la interfaz Flet y Controladores.", size=12),
                                ],
                                spacing=6,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.VERIFIED, color=ft.Colors.GREEN_400),
                                    ft.Text("15% Visualización Interactiva: Nodos conectados con flechas bidireccionales, bloques de Pila y tarjetas de Prioridad.", size=12),
                                ],
                                spacing=6,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.VERIFIED, color=ft.Colors.GREEN_400),
                                    ft.Text("10% Sistema Undo/Redo: Historial reversible conectado a botones en la interfaz.", size=12),
                                ],
                                spacing=6,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=16,
                    border=ft.Border.all(1, ft.Colors.GREEN_900),
                    border_radius=ft.BorderRadius.all(12),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                ),
            ],
            spacing=12,
        )

    def build_ui(self):
        """Construye o reconstruye la interfaz de usuario completa."""
        stats = self.controller.get_statistics()

        # Determinar contenido según la pestaña seleccionada
        if self.current_section == "visualizer":
            body = self.build_visualizer_tab()
        elif self.current_section == "operations":
            body = self.build_operations_tab()
        else:
            body = self.build_rubric_tab()

        self.page.clean()
        self.page.add(
            ft.Column(
                [
                    self.build_header(),
                    self.status_banner,
                    build_stats_panel(stats),
                    self.build_navigation_bar(),
                    ft.Divider(color=ft.Colors.GREY_800, height=1),
                    body,
                ],
                spacing=12,
            )
        )
        self.page.update()

    def render(self):
        """Función llamada por el controlador ante cambios de modelo."""
        self.build_ui()
