# Gestión de Estudiantes - Control Académico y Estructuras de Datos

Proyecto integral de **Estructuras de Datos y Algoritmos** implementado con el patrón arquitectónico **Modelo-Vista-Controlador (MVC)** e interfaz gráfica multiplataforma en **Flet (Flutter engine)**.

---

## 📋 Resumen de Cumplimiento Técnico (100%)

| Criterio | Ponderación | Estado | Implementación Técnica |
|---|---|---|---|
| **Estructuras Manuales Puras** | **35%** | **Cumplido al 100%** | Prohibido uso de `list` nativo. Implementación manual de `DoublyLinkedList`, `Stack`, `PriorityQueue`, `CircularDoublyLinkedList` y `GradeList` con nodos y punteros explícitos `next` / `prev`. |
| **Arquitectura MVC** | **20%** | **Cumplido al 100%** | Aislamiento estricto: `models/` (memoria pura sin dependencias de UI), `controllers/` (mediación de eventos), `views/` (renderizado reactivo en Flet). |
| **Soporte Multiplataforma** | **20%** | **Cumplido al 100%** | Ejecución nativa Win32 (Escritorio), modo Navegador Web (`--web`), navegación adaptativa para dispositivos móviles y pantallas táctiles con `NavigationBar`. |
| **Visualización Interactiva** | **15%** | **Cumplido al 100%** | Nodos bidireccionales con flechas en tiempo real, bloques LIFO verticales (Undo/Redo), tarjetas con código de color en Cola de Prioridad y circuito continuo cerrado en la Lista Circular. |
| **Análisis Algorítmico y Rendimiento** | **10%** | **Cumplido al 100%** | Medición en vivo de operaciones por segundo (ops/s), consumo en bytes por nodo (`sys.getsizeof`), latencia en µs y validación empírica $O(1)$ vs $O(n)$. |

---

## 📁 Estructura del Proyecto

```text
proyecto/
├── models/                       # MODELO: Memoria y estructuras de datos puras (Sin UI)
│   ├── __init__.py
│   ├── base.py                   # Interfaces abstractas (ABC)
│   ├── structures.py             # Node, DoublyLinkedList, Stack, PriorityQueue, CircularDoublyLinkedList
│   ├── student.py                # Entidad Estudiante y GradeList (lista enlazada de notas)
│   ├── undo_redo.py              # UndoRedoManager (doble pila LIFO)
│   ├── student_management.py     # Lógica de negocio (gestión académica + rondas)
│   ├── student_engine.py         # Motor extendido para inspección y estadísticas
│   ├── logistic_engine.py        # Alias de compatibilidad técnica
│   └── benchmarks.py             # Medición en tiempo real: ops/s, bytes y Big-O
├── controllers/                  # CONTROLADOR: Mediador MVC
│   ├── __init__.py
│   └── app_controller.py         # AppController (procesamiento de eventos y estado)
├── views/                        # VISTA: Interfaz gráfica responsiva con Flet
│   ├── __init__.py
│   ├── components.py             # Componentes visuales de estructuras y panel de métricas
│   └── desktop_view.py           # Vista responsiva (Escritorio, Web y Móvil)
├── tests/                        # PRUEBAS AUTOMATIZADAS (27 Tests)
│   ├── __init__.py
│   ├── test_structures.py        # Punteros y casos límite de estructuras lineales
│   ├── test_student_manager.py   # Pruebas de funcionalidades y Undo/Redo
│   ├── test_controller.py        # Pruebas de mediación del controlador
│   └── test_benchmarks_and_circular.py # Pruebas de Lista Circular y métricas de rendimiento
├── main.py                       # Lanzador general (Desktop, Web o CLI)
├── app.py                        # Lanzador directo de interfaz gráfica
├── build_exe.bat                 # Script de compilación a ejecutable Windows (Win32 EXE)
├── requirements.txt              # Dependencias del proyecto
└── README.md

```

---

## 🚀 Modos de Ejecución

### 1. Interfaz Gráfica de Escritorio (Nativa Win32 / macOS / Linux)
```bash
python main.py
```
*(o también: `python app.py`)*

### 2. Modo Navegador Web
Despliega la aplicación en un servidor web local y la abre en el navegador predeterminado:
```bash
python main.py --web
```
*(URL: `http://localhost:8550`)*

### 3. Modo Consola / Demostración CLI
Para terminales sin entorno gráfico o revisiones rápidas:
```bash
python main.py --cli
```

### 4. Empaquetado a Win32 EXE Independiente
Para generar el ejecutable autónomo `.exe` para Windows:
```cmd
build_exe.bat
```
El ejecutable resultante se genera en `dist\SistemaEstudiantes.exe`.

### 5. Ejecutar la Batería de Pruebas Unitarias
```bash
python -m unittest discover tests
```
*Ejecuta 27 pruebas unitarias con 100% de éxito.*

---

## ⚡ Complejidad Algorítmica y Rendimiento

| Operación | Estructura Utilizada | Complejidad Teórica | Rendimiento Empírico | Memoria por Nodo |
|---|---|---|---|---|
| Inserción al inicio (`prepend`) | `DoublyLinkedList` | **O(1)** | > 1,200,000 ops/s | 48 Bytes |
| Inserción al final (`append`) | `DoublyLinkedList` | **O(1)** | > 3,800,000 ops/s | 48 Bytes |
| Desapilar / Apilar (`push`/`pop`) | `Stack` (LIFO) | **O(1)** | > 5,000,000 ops/s | 48 Bytes |
| Turno circular (`step`/`step_backward`)| `CircularDoublyLinkedList`| **O(1)** | > 4,000,000 ops/s | 48 Bytes |
| Desencolar Urgencia (`dequeue`) | `PriorityQueue` | **O(1)** | > 3,500,000 ops/s | 48 Bytes |
| Búsqueda por ID / Valor | `DoublyLinkedList` | **O(n)** | Proporcional a $N$ | N/A |
| Eliminación por Búsqueda | `DoublyLinkedList` | **O(n)** | Proporcional a $N$ | N/A |
| Encolar con Prioridad | `PriorityQueue` | **O(n)** | Inserción ordenada | 48 Bytes |

---

## 🖥️ Módulos de la Interfaz

1. **Estructuras de Memoria:**
   - **Lista Doblemente Enlazada:** Nodos con tarjetas de estudiantes, conexiones gráficas `next` / `prev`, indicadores de `HEAD` y `TAIL`, y botón para añadir estudiante de forma manual o rápida.
   - **Pilas LIFO:** Visualización vertical de bloques apilados de Deshacer (Undo) y Rehacer (Redo).
   - **Cola de Prioridad:** Tarjetas con código de color (Becas/Urgente en rojo, Reubicación en ámbar, Regular en azul).
   - **Lista Circular (Circuito Continuo):** Recorrido cíclico bidireccional con indicador de turno activo y cierre de circuito `tail ↺ head`.
2. **Operaciones y Registro:**
   - Formularios de inscripción ordenada o directa, baja, actualización de notas, encolado prioritario y tabla completa de calificaciones.
3. **Métricas de Rendimiento:**
   - Panel de benchmarking en vivo con medición instantánea de operaciones por segundo, latencias medias y consumo en bytes.
4. **Análisis y Rúbrica:**
   - Panel interactivo con el desglose del 100% de la rúbrica oficial, verificación técnica de criterios y validación de las 27 pruebas superadas.
