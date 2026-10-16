"""Punto de entrada principal del proyecto (Semanas 1, 2 y 3).
Arquitectura MVC - Estructuras de Datos Lineales Puras.
Modos de ejecución:
- Escritorio Nativo (Win32): python main.py
- Navegador Web:             python main.py --web
- Consola (CLI):             python main.py --cli
"""

import sys
from models.student_engine import StudentEngine
from controllers.app_controller import AppController


def run_gui(web_mode: bool = False):
    """Inicia la interfaz gráfica en modo Escritorio o Navegador Web."""
    try:
        import flet as ft
        from views.desktop_view import DesktopView

        def gui_main(page: ft.Page):
            engine = StudentEngine(sort_by="apellido")
            engine.seed_sample_data()
            controller = AppController(engine=engine)
            DesktopView(page=page, controller=controller)

        if hasattr(ft, "run"):
            if web_mode:
                print("[INFO] Iniciando servidor Web Flet en navegador: http://localhost:8550")
                ft.run(gui_main, view=ft.AppView.WEB_BROWSER, port=8550)
            else:
                ft.run(gui_main)
        elif hasattr(ft, "app"):
            if web_mode:
                ft.app(target=gui_main, view=ft.AppView.WEB_BROWSER, port=8550)
            else:
                ft.app(target=gui_main)
        else:
            raise RuntimeError("No se encontró el lanzador de Flet.")
    except Exception as e:
        print(f"[AVISO] No se pudo iniciar la interfaz gráfica: {e}")
        print("Iniciando modo demostración por consola (CLI)...")
        run_cli_demo()


def run_cli_demo():
    """Demostración de consola para terminales sin soporte gráfico."""
    print("=" * 65)
    print(" SIMULADOR DE GESTION DE ESTUDIANTES - SEMANAS 1, 2 Y 3")
    print(" Arquitectura MVC - Estructuras Lineales Puras - Doble Pila")
    print("=" * 65)

    controller = AppController(StudentEngine(sort_by="apellido"))

    print("\n[1] Inscribiendo Estudiantes desde el Controlador...")
    controller.inscribir_estudiante("EST-101", "Maria", "Gonzalez", "18.5, 19.0, 17.0")
    controller.inscribir_estudiante("EST-102", "Alejandro", "Barrios", "14.0, 15.5, 13.0")
    controller.inscribir_estudiante("EST-103", "Camila", "Diaz", "20.0, 19.5, 19.0")
    controller.inscribir_estudiante("EST-104", "Esteban", "Torres", "11.0, 12.0, 10.5")
    print("[OK] Estudiantes inscritos.")

    print("\n[2] Reporte de Lista Doblemente Enlazada:")
    print(controller.model.generar_reporte_texto())

    print("\n[3] Probando Undo / Redo:")
    print("Eliminando a EST-102...")
    controller.dar_de_baja("EST-102")
    print("<- Deshaciendo baja:")
    undo_res = controller.deshacer()
    print(undo_res["message"])

    print("\n[4] Probando Cola de Prioridad:")
    controller.encolar_admision_prioritaria("ESP-01", "Javier", "Paz (Beca)", 9.5)
    controller.encolar_admision_prioritaria("ESP-02", "Lucia", "Mendez", 3.0)
    atendido = controller.atender_siguiente_prioridad()
    print(atendido["message"])

    print("\n[5] Probando Benchmark de Rendimiento (Semana 3):")
    bench = controller.run_benchmarks(iterations=1000)
    print(f"Memoria por nodo: {bench['memory']['node_bytes']} bytes")
    for b in bench["benchmarks"][:3]:
        print(f" - {b['estructura']} {b['operacion']}: {b['ops_segundo']:,} ops/s ({b['complejidad']})")

    print("\n" + "=" * 65)
    print(" Para abrir la interfaz grafica completa:")
    print(" - Escritorio: python main.py  (o python app.py)")
    print(" - Navegador:  python main.py --web")
    print("=" * 65)


if __name__ == "__main__":
    args = sys.argv[1:]
    if any(a in args for a in ("--cli", "--demo", "-c")):
        run_cli_demo()
    elif any(a in args for a in ("--web", "-w", "--browser")):
        run_gui(web_mode=True)
    else:
        run_gui(web_mode=False)
