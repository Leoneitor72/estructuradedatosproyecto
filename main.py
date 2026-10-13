"""Punto de entrada principal del proyecto (Semana 1 y Semana 2).
Por defecto inicia la aplicación de escritorio Flet con arquitectura MVC.
Si se pasa el argumento `--cli`, ejecuta la demostración en consola.
"""

import sys
from models.student_engine import StudentEngine
from controllers.app_controller import AppController


def run_gui():
    """Inicia la interfaz gráfica de escritorio con Flet."""
    try:
        import flet as ft
        from views.desktop_view import DesktopView

        def gui_main(page: ft.Page):
            engine = StudentEngine(sort_by="apellido")
            engine.seed_sample_data()
            controller = AppController(engine=engine)
            DesktopView(page=page, controller=controller)

        if hasattr(ft, "run"):
            ft.run(gui_main)
        elif hasattr(ft, "app"):
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
    print(" SIMULADOR DE GESTION DE ESTUDIANTES - SEMANA 1 Y SEMANA 2")
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

    print("\n" + "=" * 65)
    print(" Para abrir la interfaz grafica completa con Flet:")
    print(" Ejecuta: python main.py  (o python app.py)")
    print("=" * 65)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--cli", "--demo", "-c"):
        run_cli_demo()
    else:
        run_gui()
