"""Componentes Visuales en Flet para Estructuras de Datos (Semana 2 - Día 3).
Representación gráfica interactiva:
- Vista gráfica de Lista Doblemente Enlazada (nodos con flechas bidireccionales).
- Vista gráfica de Pila (bloques apilados verticalmente LIFO).
- Vista gráfica de Cola de Prioridad (tarjetas horizontales con código de color por prioridad).
- Vista gráfica de Cola Circular (turnos cíclicos Round-Robin).
"""

from typing import List, Dict, Any, Optional, Callable
import flet as ft


def build_doubly_linked_list_view(
    nodes_data: List[Dict[str, Any]],
    on_delete_callback: Optional[Callable[[str], None]] = None,
) -> ft.Control:
    """Semana 2 - Día 3: Vista gráfica de Lista Doblemente Enlazada.
    Representa visualmente cada nodo enlazado con flechas bidireccionales prev y next.
    """
    if not nodes_data:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ACCOUNT_TREE_OUTLINED, size=48, color=ft.Colors.BLUE_300),
                    ft.Text(
                        "La Lista Doblemente Enlazada está vacía (head = None, tail = None)",
                        color=ft.Colors.GREY_400,
                        size=14,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        "Inscribe un estudiante para ver cómo se crean los nodos y punteros.",
                        color=ft.Colors.GREY_600,
                        size=12,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            alignment=ft.Alignment(0, 0),
            padding=30,
            border=ft.Border.all(1, ft.Colors.BLUE_900),
            border_radius=ft.BorderRadius.all(12),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )

    row_controls: List[ft.Control] = []

    # Indicador de puntero inicial HEAD ->
    row_controls.append(
        ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("HEAD", color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.BLUE_600,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                        border_radius=ft.BorderRadius.all(6),
                    ),
                    ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.BLUE_400, size=22),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.Padding.only(right=10),
        )
    )

    for i, node in enumerate(nodes_data):
        # Estilo según posición
        is_head = node.get("is_head", False)
        is_tail = node.get("is_tail", False)
        prom = node.get("promedio", 0.0)

        # Color de promedio
        if prom >= 16.0:
            prom_color = ft.Colors.GREEN_400
        elif prom >= 11.0:
            prom_color = ft.Colors.AMBER_400
        else:
            prom_color = ft.Colors.RED_400

        # Tarjeta del nodo
        node_card = ft.Container(
            content=ft.Column(
                [
                    # Encabezado del nodo (Puntero prev)
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    f"prev: {node['prev_id'] or 'None'}",
                                    size=10,
                                    color=ft.Colors.PURPLE_200 if node["prev_id"] else ft.Colors.RED_300,
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text("HEAD", size=9, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                            bgcolor=ft.Colors.BLUE_700,
                                            padding=ft.Padding.symmetric(horizontal=4, vertical=1),
                                            border_radius=ft.BorderRadius.all(4),
                                            visible=is_head,
                                        ),
                                        ft.Container(
                                            content=ft.Text("TAIL", size=9, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                                            bgcolor=ft.Colors.AMBER_400,
                                            padding=ft.Padding.symmetric(horizontal=4, vertical=1),
                                            border_radius=ft.BorderRadius.all(4),
                                            visible=is_tail,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor=ft.Colors.BLACK_54,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                        border_radius=ft.BorderRadius.only(top_left=8, top_right=8),
                    ),
                    # Cuerpo del nodo (Datos de Estudiante)
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_300, size=20),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    f"{node['apellido']}, {node['nombre']}",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.WHITE,
                                                    no_wrap=True,
                                                ),
                                                ft.Text(
                                                    f"ID: {node['id']}",
                                                    size=11,
                                                    color=ft.Colors.BLUE_200,
                                                ),
                                            ],
                                            spacing=1,
                                        ),
                                    ],
                                    spacing=6,
                                ),
                                ft.Row(
                                    [
                                        ft.Text("Promedio:", size=11, color=ft.Colors.GREY_300),
                                        ft.Container(
                                            content=ft.Text(
                                                f"{prom:.2f}",
                                                size=11,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.WHITE,
                                            ),
                                            bgcolor=prom_color,
                                            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                            border_radius=ft.BorderRadius.all(4),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text(
                                    f"Notas: {', '.join(f'{n:.1f}' for n in node.get('notas', [])) or 'Sin notas'}",
                                    size=10,
                                    color=ft.Colors.GREY_400,
                                    no_wrap=True,
                                ),
                            ],
                            spacing=6,
                        ),
                        padding=10,
                    ),
                    # Pie del nodo (Puntero next y botón dar de baja)
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    f"next: {node['next_id'] or 'None'}",
                                    size=10,
                                    color=ft.Colors.GREEN_200 if node["next_id"] else ft.Colors.RED_300,
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_300,
                                    icon_size=16,
                                    tooltip=f"Dar de baja a {node['id']}",
                                    on_click=lambda _, nid=node["id"]: on_delete_callback(nid)
                                    if on_delete_callback
                                    else None,
                                    visible=on_delete_callback is not None,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor=ft.Colors.BLACK_54,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                        border_radius=ft.BorderRadius.only(bottom_left=8, bottom_right=8),
                    ),
                ],
                spacing=0,
            ),
            width=210,
            border=ft.Border.all(
                2 if (is_head or is_tail) else 1,
                ft.Colors.AMBER_400 if is_tail else (ft.Colors.BLUE_500 if is_head else ft.Colors.BLUE_800),
            ),
            border_radius=ft.BorderRadius.all(10),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )
        row_controls.append(node_card)

        # Si no es el último nodo, dibujar flechas bidireccionales entre nodos
        if i < len(nodes_data) - 1:
            arrow_connector = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("── next ──►", size=10, color=ft.Colors.GREEN_400, weight=ft.FontWeight.BOLD),
                        ft.Text("◄── prev ──", size=10, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                padding=ft.Padding.symmetric(horizontal=8),
            )
            row_controls.append(arrow_connector)

    # Indicador de puntero final -> TAIL
    row_controls.append(
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ARROW_BACK, color=ft.Colors.AMBER_400, size=22),
                    ft.Container(
                        content=ft.Text("TAIL", color=ft.Colors.BLACK, size=11, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.AMBER_400,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                        border_radius=ft.BorderRadius.all(6),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.Padding.only(left=10),
        )
    )

    return ft.Container(
        content=ft.Row(
            controls=row_controls,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=14,
        border=ft.Border.all(1, ft.Colors.BLUE_900),
        border_radius=ft.BorderRadius.all(12),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    )


def build_stack_view(
    stack_items: List[str],
    title: str = "Historial Deshacer (Undo Stack)",
    is_undo: bool = True,
) -> ft.Control:
    """Semana 2 - Día 3: Vista gráfica de Pila (bloques apilados verticalmente LIFO)."""
    blocks: List[ft.Control] = []

    if not stack_items:
        blocks.append(
            ft.Container(
                content=ft.Text(
                    "(Pila vacía)",
                    size=12,
                    color=ft.Colors.GREY_500,
                    italic=True,
                ),
                padding=12,
                alignment=ft.Alignment(0, 0),
            )
        )
    else:
        for idx, desc in enumerate(stack_items):
            is_top = idx == 0
            block_color = (
                ft.Colors.BLUE_700 if (is_undo and is_top)
                else (ft.Colors.PURPLE_700 if is_top else ft.Colors.SURFACE_CONTAINER_HIGHEST)
            )

            blocks.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(
                                    "TOP" if is_top else f"#{len(stack_items) - idx}",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                bgcolor=ft.Colors.BLUE_500 if is_top else ft.Colors.BLACK_45,
                                padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                border_radius=ft.BorderRadius.all(4),
                            ),
                            ft.Text(
                                desc,
                                size=11,
                                color=ft.Colors.WHITE if is_top else ft.Colors.GREY_300,
                                weight=ft.FontWeight.W_600 if is_top else ft.FontWeight.NORMAL,
                                no_wrap=True,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=block_color,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                    border=ft.Border.all(
                        1.5 if is_top else 1,
                        ft.Colors.BLUE_400 if (is_undo and is_top) else ft.Colors.GREY_700,
                    ),
                    border_radius=ft.BorderRadius.all(8),
                    margin=ft.Margin.symmetric(vertical=2, horizontal=0),
                )
            )

    # Base de la pila
    blocks.append(
        ft.Container(
            content=ft.Text("══ BASE DE LA PILA (LIFO) ══", size=10, color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding.only(top=6),
        )
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.LAYERS if is_undo else ft.Icons.HISTORY,
                            size=18,
                            color=ft.Colors.BLUE_300 if is_undo else ft.Colors.PURPLE_300,
                        ),
                        ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Container(
                            content=ft.Text(f"{len(stack_items)}", size=10, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_600 if is_undo else ft.Colors.PURPLE_600,
                            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                            border_radius=ft.BorderRadius.all(10),
                        ),
                    ],
                    spacing=6,
                ),
                ft.Divider(color=ft.Colors.GREY_800, height=1),
                ft.Column(controls=blocks, spacing=2, scroll=ft.ScrollMode.AUTO),
            ],
            spacing=8,
        ),
        padding=12,
        border=ft.Border.all(1, ft.Colors.BLUE_900 if is_undo else ft.Colors.PURPLE_900),
        border_radius=ft.BorderRadius.all(12),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        height=230,
    )


def build_priority_queue_view(
    priority_items: List[Dict[str, Any]],
    on_attend_callback: Optional[Callable[[], None]] = None,
) -> ft.Control:
    """Semana 2 - Día 3: Vista gráfica de Cola de Prioridad.
    Tarjetas ordenadas horizontalmente con código de color por prioridad.
    """
    card_controls: List[ft.Control] = []

    if not priority_items:
        card_controls.append(
            ft.Container(
                content=ft.Text(
                    "No hay solicitudes pendientes en la cola de prioridad.",
                    size=12,
                    color=ft.Colors.GREY_500,
                    italic=True,
                ),
                padding=16,
            )
        )
    else:
        for idx, item in enumerate(priority_items):
            est = item["estudiante"]
            prioridad = item["prioridad"]
            is_head = idx == 0

            # Código de color por prioridad
            if prioridad >= 8.0:
                card_bg = ft.Colors.RED_900
                border_color = ft.Colors.RED_400
                badge_text = "ALTA / BECA"
                badge_bg = ft.Colors.RED_500
            elif prioridad >= 5.0:
                card_bg = ft.Colors.AMBER_900
                border_color = ft.Colors.AMBER_400
                badge_text = "MEDIA"
                badge_bg = ft.Colors.AMBER_600
            else:
                card_bg = ft.Colors.BLUE_900
                border_color = ft.Colors.BLUE_400
                badge_text = "REGULAR"
                badge_bg = ft.Colors.BLUE_600

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        "HEAD (Próximo)" if is_head else f"#{idx+1}",
                                        size=9,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=ft.Colors.GREEN_600 if is_head else ft.Colors.BLACK_54,
                                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=ft.BorderRadius.all(4),
                                ),
                                ft.Container(
                                    content=ft.Text(badge_text, size=9, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    bgcolor=badge_bg,
                                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=ft.BorderRadius.all(4),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(
                            f"{est.nombre} {est.apellido}",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            no_wrap=True,
                        ),
                        ft.Row(
                            [
                                ft.Text(f"ID: {est.id}", size=11, color=ft.Colors.GREY_300),
                                ft.Text(f"Score: {prioridad:.1f}", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_300),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=6,
                ),
                width=175,
                padding=10,
                border=ft.Border.all(1.5 if is_head else 1, border_color),
                border_radius=ft.BorderRadius.all(8),
                bgcolor=card_bg,
            )
            card_controls.append(card)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.LOW_PRIORITY, size=18, color=ft.Colors.AMBER_400),
                                ft.Text(
                                    "Cola de Prioridad (Admisiones Especiales / Becas)",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Container(
                                    content=ft.Text(f"{len(priority_items)} en espera", size=10, color=ft.Colors.WHITE),
                                    bgcolor=ft.Colors.AMBER_800,
                                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=ft.BorderRadius.all(10),
                                ),
                            ],
                            spacing=6,
                        ),
                        ft.FilledButton(
                            content="Atender Siguiente (O(1))",
                            icon=ft.Icons.CHECK,
                            on_click=lambda _: on_attend_callback() if on_attend_callback else None,
                            disabled=len(priority_items) == 0,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(color=ft.Colors.GREY_800, height=1),
                ft.Row(controls=card_controls, scroll=ft.ScrollMode.AUTO, spacing=8),
            ],
            spacing=8,
        ),
        padding=12,
        border=ft.Border.all(1, ft.Colors.AMBER_900),
        border_radius=ft.BorderRadius.all(12),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    )


def build_circular_queue_view(
    circular_nodes: List[Dict[str, Any]],
    current_turn: Optional[Dict[str, Any]] = None,
    on_step_callback: Optional[Callable[[], None]] = None,
    on_prev_callback: Optional[Callable[[], None]] = None,
) -> ft.Control:
    """Semana 3 - Día 2: Vista gráfica animada de la Lista Doblemente Enlazada Circular (Circuito continuo)."""
    cards: List[ft.Control] = []

    if not circular_nodes:
        cards.append(
            ft.Container(
                content=ft.Text("La cola circular está vacía. Inscribe alumnos para iniciar el circuito.", color=ft.Colors.GREY_500, italic=True),
                padding=12,
            )
        )
    else:
        for i, node in enumerate(circular_nodes):
            is_active = node.get("is_current", False)
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text("TURNO ACTIVO" if is_active else f"Parada #{i+1}", size=9, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    bgcolor=ft.Colors.CYAN_700 if is_active else ft.Colors.BLACK_54,
                                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=ft.BorderRadius.all(4),
                                ),
                                ft.Text(f"Prom: {node['promedio']:.2f}", size=10, color=ft.Colors.CYAN_200, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(f"{node['nombre']} {node['apellido']}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, no_wrap=True),
                        ft.Text(f"ID: {node['id']}", size=11, color=ft.Colors.GREY_300),
                        ft.Row(
                            [
                                ft.Text(f"◄ {node['prev_id'] or 'tail'}", size=9, color=ft.Colors.PURPLE_200),
                                ft.Text(f"{node['next_id'] or 'head'} ►", size=9, color=ft.Colors.GREEN_200),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=4,
                ),
                width=170,
                padding=8,
                border=ft.Border.all(2 if is_active else 1, ft.Colors.CYAN_400 if is_active else ft.Colors.CYAN_800),
                border_radius=ft.BorderRadius.all(8),
                bgcolor=ft.Colors.CYAN_950 if is_active else ft.Colors.SURFACE_CONTAINER_HIGHEST,
            )
            cards.append(card)
            if i < len(circular_nodes) - 1:
                cards.append(
                    ft.Text("◄──►", size=11, color=ft.Colors.CYAN_400, weight=ft.FontWeight.BOLD)
                )

        cards.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ALL_INCLUSIVE, size=18, color=ft.Colors.CYAN_300),
                        ft.Text("tail ↺ head", size=10, color=ft.Colors.CYAN_300, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=4,
                ),
                padding=ft.Padding.symmetric(horizontal=6),
            )
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.SYNC, color=ft.Colors.CYAN_300, size=22),
                                ft.Column(
                                    [
                                        ft.Text("Ruta Circular Bidireccional (Circular Doubly Linked List)", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("Circuito continuo sin fin de lista: tail.next = head y head.prev = tail", size=11, color=ft.Colors.GREY_400),
                                    ],
                                    spacing=1,
                                ),
                            ],
                            spacing=6,
                        ),
                        ft.Row(
                            [
                                ft.FilledButton(
                                    content="◄ Anterior",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda _: on_prev_callback() if on_prev_callback else None,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_800),
                                ),
                                ft.FilledButton(
                                    content="Siguiente ►",
                                    icon=ft.Icons.ARROW_FORWARD,
                                    on_click=lambda _: on_step_callback() if on_step_callback else None,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700),
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(color=ft.Colors.GREY_800, height=1),
                ft.Row(controls=cards, scroll=ft.ScrollMode.AUTO, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            ],
            spacing=8,
        ),
        padding=12,
        border=ft.Border.all(1, ft.Colors.CYAN_900),
        border_radius=ft.BorderRadius.all(12),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    )


def build_benchmark_panel(
    benchmark_data: Optional[Dict[str, Any]],
    on_run_benchmark: Optional[Callable[[], None]] = None,
) -> ft.Control:
    """Semana 3 - Día 3: Panel de métricas de rendimiento en tiempo real O(1) vs O(n) y memoria."""
    rows: List[ft.DataRow] = []
    benchmarks = benchmark_data.get("benchmarks", []) if benchmark_data else []
    memory = benchmark_data.get("memory", {}) if benchmark_data else {}

    for b in benchmarks:
        is_o1 = b["complejidad"] == "O(1)"
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(b["operacion"], weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(b["estructura"])),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(b["complejidad"], size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREEN_700 if is_o1 else ft.Colors.AMBER_700,
                            padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                            border_radius=ft.BorderRadius.all(4),
                        )
                    ),
                    ft.DataCell(ft.Text(f"{b['ops_segundo']:,} ops/s", weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300)),
                    ft.DataCell(ft.Text(f"{b['tiempo_por_op_us']:.3f} µs")),
                    ft.DataCell(ft.Text(f"{b['tiempo_total_ms']} ms ({b['operaciones']} ops)", color=ft.Colors.GREY_400)),
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Operación")),
            ft.DataColumn(ft.Text("Estructura")),
            ft.DataColumn(ft.Text("Big-O Teórico")),
            ft.DataColumn(ft.Text("Operaciones / seg")),
            ft.DataColumn(ft.Text("Latencia Promedio")),
            ft.DataColumn(ft.Text("Tiempo Batería")),
        ],
        rows=rows,
        border=ft.Border.all(1, ft.Colors.GREY_800),
        border_radius=ft.BorderRadius.all(8),
        heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )

    node_mem = memory.get("node_bytes", 48)
    pnode_mem = memory.get("priority_node_bytes", 48)

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.SPEED, size=24, color=ft.Colors.GREEN_400),
                                ft.Column(
                                    [
                                        ft.Text("Panel de Métricas y Rendimiento en Tiempo Real (Semana 3)", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        ft.Text("Comparación de Complejidad Temporal Empírica O(1) vs O(n) y Consumo de Memoria por Nodo", size=11, color=ft.Colors.GREY_400),
                                    ],
                                    spacing=1,
                                ),
                            ],
                            spacing=6,
                        ),
                        ft.FilledButton(
                            content="Ejecutar Benchmark en Vivo",
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=lambda _: on_run_benchmark() if on_run_benchmark else None,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(color=ft.Colors.GREY_800, height=1),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Memoria por Nodo (Punteros)", size=11, color=ft.Colors.GREY_400),
                                    ft.Text(f"{node_mem} Bytes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300),
                                    ft.Text("data + next + prev (sys.getsizeof)", size=10, color=ft.Colors.GREY_500),
                                ],
                                spacing=2,
                            ),
                            padding=10,
                            border=ft.Border.all(1, ft.Colors.CYAN_800),
                            border_radius=ft.BorderRadius.all(8),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Memoria Nodo Prioridad", size=11, color=ft.Colors.GREY_400),
                                    ft.Text(f"{pnode_mem} Bytes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_300),
                                    ft.Text("data + priority + next + prev", size=10, color=ft.Colors.GREY_500),
                                ],
                                spacing=2,
                            ),
                            padding=10,
                            border=ft.Border.all(1, ft.Colors.AMBER_800),
                            border_radius=ft.BorderRadius.all(8),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Modelo de Punteros", size=11, color=ft.Colors.GREY_400),
                                    ft.Text("64-Bit Reference Model", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_300),
                                    ft.Text("Sin fragmentación por reasignación dinámica", size=10, color=ft.Colors.GREY_500),
                                ],
                                spacing=2,
                            ),
                            padding=10,
                            border=ft.Border.all(1, ft.Colors.GREEN_800),
                            border_radius=ft.BorderRadius.all(8),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(
                    content=table if rows else ft.Text("Presione 'Ejecutar Benchmark en Vivo' para iniciar la medición de operaciones por segundo.", color=ft.Colors.GREY_400, italic=True),
                    padding=4,
                ),
            ],
            spacing=10,
        ),
        padding=12,
        border=ft.Border.all(1, ft.Colors.GREEN_900),
        border_radius=ft.BorderRadius.all(12),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    )



def build_stats_panel(stats: Dict[str, Any]) -> ft.Control:
    """Panel resumen con métricas clave del centro educativo."""
    total = stats.get("total", 0)
    prom_gen = stats.get("promedio_general", 0.0)
    mejor = stats.get("mejor_estudiante")
    menor = stats.get("menor_estudiante")

    def stat_card(label: str, value: str, icon: str, color: str):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=color, size=28),
                    ft.Column(
                        [
                            ft.Text(label, size=11, color=ft.Colors.GREY_400),
                            ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        spacing=1,
                    ),
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            border=ft.Border.all(1, ft.Colors.GREY_800),
            border_radius=ft.BorderRadius.all(8),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            expand=True,
        )

    mejor_str = f"{mejor.nombre} ({mejor.calcular_promedio():.2f})" if mejor else "N/A"
    menor_str = f"{menor.nombre} ({menor.calcular_promedio():.2f})" if menor else "N/A"

    return ft.Row(
        [
            stat_card("Total Inscritos", str(total), ft.Icons.PEOPLE_ALT, ft.Colors.BLUE_400),
            stat_card("Promedio Global", f"{prom_gen:.2f}", ft.Icons.ANALYTICS, ft.Colors.GREEN_400),
            stat_card("Mejor Rendimiento", mejor_str, ft.Icons.STAR, ft.Colors.AMBER_400),
            stat_card("Rendimiento Bajo", menor_str, ft.Icons.WARNING_AMBER, ft.Colors.RED_400),
        ],
        spacing=8,
    )
