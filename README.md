# Sistema de Gestión de Estudiantes - Semanas 1 y 2

Proyecto educativo de **Estructuras de Datos y Algoritmos** bajo el patrón **Modelo-Vista-Controlador (MVC)** con interfaz gráfica multiplataforma en **Flet (Flutter engine)**.

---

## 📋 Resumen de Cumplimiento de Rúbrica

| Criterio | Ponderación | Estado | Implementación |
|---|---|---|---|
| **Estructuras Manuales Puras** | **35%** | **Cumplido al 100%** | Prohibido uso de `list` nativo. Listas Doblemente Enlazadas, Pilas, Colas de Prioridad y Notas con clases `Node` y punteros explícitos. |
| **Arquitectura MVC** | **20%** | **Cumplido al 100%** | Aislamiento total: `models/` (memoria pura), `controllers/` (mediación de eventos), `views/` (interfaz Flet). |
| **Visualización Dinámica** | **15%** | **Cumplido al 100%** | Nodos con flechas bidireccionales `next`/`prev`, bloques apilados verticales de Pila, tarjetas con color por prioridad y turno circular. |
| **Sistema Undo/Redo** | **10%** | **Cumplido al 100%** | Doble Pila LIFO conectada a botones interactivos en la interfaz y en consola. |
| **Pruebas y Usabilidad** | **20%** | **Cumplido al 100%** | 25 pruebas unitarias con `unittest` (100% cobertura de punteros y controlador) y ejecución nativa en escritorio. |

---

## 📁 Estructura del Proyecto (MVC)

```text
proyecto/
├── models/                       # MODELO: Lógica pura de estructuras y memoria (Sin UI)
│   ├── __init__.py
│   ├── base.py                   # Interfaces abstractas (ABC)
│   ├── structures.py             # Node, DoublyLinkedList, Stack, PriorityQueue, CircularQueue
│   ├── student.py                # Estudiante y GradeList (lista enlazada propia de notas)
│   ├── undo_redo.py              # UndoRedoManager (doble pila LIFO)
│   ├── student_management.py     # Gestor de las 5 funcionalidades base
│   ├── student_engine.py         # Motor extendido para inspección y estadísticas UI
│   └── logistic_engine.py        # Alias de compatibilidad según rúbrica del PDF
├── controllers/                  # CONTROLADOR: Mediador entre interfaz y modelo
│   ├── __init__.py
│   └── app_controller.py         # AppController (procesamiento de eventos y estado)
├── views/                        # VISTA: Interfaz gráfica responsiva con Flet
│   ├── __init__.py
│   ├── components.py             # Componentes visuales de Pila, Cola, Lista Doble
│   └── desktop_view.py           # Vista de escritorio Win32 / macOS / Linux
├── tests/                        # PRUEBAS AUTOMATIZADAS
│   ├── __init__.py
│   ├── test_structures.py        # Pruebas de punteros y estructuras puras
│   ├── test_student_manager.py   # Pruebas de las 5 funcionalidades y Undo/Redo
│   └── test_controller.py        # Pruebas de mediación del controlador
├── main.py                       # Lanzador principal (inicia la GUI de Flet o CLI)
├── app.py                        # Lanzador directo de la interfaz Flet
├── entrega_semana1.py             # Script unificado para defensa rápida
├── requirements.txt              # flet, pytest
└── README.md
```

---

## 🚀 Cómo Ejecutar la Aplicación

### 1. Iniciar la Interfaz Gráfica de Escritorio (Flet)
```bash
python main.py
```
o también:
```bash
python app.py
```

### 2. Ejecutar la Demostración en Consola (CLI)
Si deseas ejecutar la prueba interactiva por terminal:
```bash
python main.py --cli
```

### 3. Ejecutar las Pruebas Unitarias Automatizadas
Para verificar los 25 tests unitarios:
```bash
python -m unittest discover tests
```

---

## 🎯 Componentes Visuales Desarrollados en Flet (Semana 2)

1. **Visualizador de Lista Doblemente Enlazada:**
   * Representa cada nodo de estudiante con sus referencias `prev` y `next`.
   * Flechas gráficas bidireccionales (`next` en verde hacia adelante, `prev` en violeta hacia atrás).
   * Identificadores visuales de `HEAD` y `TAIL`.
2. **Visualizador de Pila (Stack LIFO):**
   * Bloques apilados verticalmente mostrando el bloque superior (`TOP`) y la base de la pila.
   * Visualización simultánea de la Pila de Deshacer (Undo) y la Pila de Rehacer (Redo).
3. **Visualizador de Cola de Prioridad:**
   * Tarjetas ordenadas de izquierda a derecha por nivel de urgencia o mérito académico.
   * Código de color: Rojo/Beca ($\ge 8.0$), Ámbar/Reubicación ($\ge 5.0$), Azul/Regular ($< 5.0$).
   * Botón de atención en tiempo constante $O(1)$.
4. **Visualizador de Cola Circular:**
   * Control dinámico de turnos para evaluación cíclica de estudiantes (Round-Robin).
5. **Botones de Deshacer y Rehacer (Undo/Redo):**
   * Botones en la barra superior con contador en vivo de acciones disponibles.
