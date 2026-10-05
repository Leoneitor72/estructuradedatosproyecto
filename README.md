# Sistema de Gestión de Estudiantes - Semana 1

Proyecto educativo de **Estructuras de Datos y Algoritmos** bajo el patrón **Modelo-Vista-Controlador (MVC)**.
En esta **Semana 1**, se implementa el **Modelo Base** y las **Estructuras de Datos Lineales Puras**.

---

## 📋 Reglas Cumplidas de la Rúbrica

1. **Implementación Manual Estricta (35%):**
   * **Prohibido el uso de `list` nativo de Python** como estructura subyacente de almacenamiento.
   * Todos los contenedores están implementados con clases `Node` / `PriorityNode` y punteros explícitos (`next`, `prev`).
   * Incluso las notas individuales del estudiante están gestionadas mediante una lista enlazada dedicada (`GradeList`).

2. **Arquitectura MVC Pura (20%):**
   * El paquete `models/` es completamente independiente de la interfaz gráfica (Flet/Flutter).
   * Lógica de memoria y punteros aislada sin dependencias de presentación.

3. **Manejo Seguro de Punteros:**
   * Las inserciones y eliminaciones contemplan todos los casos límite: lista vacía, un solo elemento, eliminar cabeza, eliminar cola y nodos intermedios, reconectando `next` y `prev` sin pérdida de referencias.

---

## 🎯 Funcionalidades Implementadas (Semana 1)

Basado en el requerimiento del **Sistema de Gestión de Estudiantes**:

| # | Funcionalidad | Descripción | Estructura / Complejidad |
|---|---|---|---|
| **1** | **Inscribir Estudiante** | Añade un estudiante con ID, nombre, apellido y notas. Permite inserción al final o mantener la lista ordenada por ID o Apellido. | `DoublyLinkedList.append` $O(1)$ / `insert_ordered` $O(n)$ |
| **2** | **Dar de Baja** | Elimina a un estudiante de la lista a partir de su ID reconectando punteros. | `DoublyLinkedList.remove` $O(n)$ búsqueda, $O(1)$ reconexión |
| **3** | **Actualizar Calificaciones** | Localiza al estudiante y actualiza su lista de notas (`GradeList`). | `GradeList.clear` + inserción $O(k)$ |
| **4** | **Calcular Promedio** | Recorre la lista de calificaciones del estudiante sumando y dividiendo entre el tamaño. | $O(k)$ donde $k$ es el número de notas |
| **5** | **Generar Reporte** | Recorre secuencialmente todos los nodos de la lista de estudiantes generando un resumen completo. | $O(n)$ recorrido por punteros |
| **+** | **Deshacer / Rehacer (Undo/Redo)** | Permite deshacer y rehacer inscripciones, bajas y actualizaciones de notas. | Doble Pila `Stack` (LIFO) $O(1)$ |
| **+** | **Cola de Admisiones Prioritarias** | Cola ordenada para procesar solicitudes prioritarias de ingreso o becas. | `PriorityQueue` $O(n)$ encolar, $O(1)$ atender |
| **+** | **Ronda de Revisión Cíclica** | Cola circular con punteros `tail.next = head` para turnos continuos. | `CircularQueue` $O(1)$ paso Round-Robin |

---

## 📁 Estructura del Proyecto

```text
proyecto-semana-1/
├── models/
│   ├── __init__.py               # Exportación del paquete de modelos
│   ├── base.py                   # Interfaces abstractas (ABC)
│   ├── structures.py             # Node, DoublyLinkedList, Stack, PriorityQueue, CircularQueue
│   ├── student.py                # Estudiante y GradeList (lista enlazada de notas)
│   ├── undo_redo.py              # UndoRedoManager (doble pila LIFO)
│   └── student_management.py     # Motor lógico del sistema de estudiantes
├── tests/
│   ├── __init__.py
│   ├── test_structures.py        # Pruebas de punteros, casos límite y colas
│   └── test_student_manager.py   # Pruebas de las 5 funcionalidades + Undo/Redo
├── main.py                       # Demostración interactiva en consola
├── requirements.txt              # flet, pytest
└── README.md
```

---

## 🧪 Ejecución de Pruebas Unitarias

Para ejecutar la batería completa de 20 pruebas unitarias con cobertura exhaustiva:

```bash
python -m unittest discover tests
```

O si utilizas pytest:

```bash
python -m pytest tests/
```

---

## 🚀 Demostración en Consola

Puedes ejecutar el archivo de demostración para ver el funcionamiento en tiempo real:

```bash
python main.py
```

---

## 🔭 Próximos Pasos (Semana 2 y Semana 3)
* **Semana 2:** Integración del Controlador (`controllers/app_controller.py`) y creación de la Vista interactiva con **Flet** (bloques de nodos, flechas visuales de punteros, tarjetas con colores de prioridad y botones interactivos de Undo/Redo).
* **Semana 3:** Despliegue multiplataforma (Windows Desktop Win32, Navegador Web y Móvil) y panel de análisis de métricas en tiempo real.
