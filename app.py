"""Punto de entrada de la Aplicación Multiplataforma Flet - Gestión de Estudiantes.
Ejecuta la interfaz nativa en Windows (Win32), macOS, Linux o Navegador Web.
"""

import sys
import flet as ft
from models.student_engine import StudentEngine
from controllers.app_controller import AppController
from views.desktop_view import DesktopView


def main(page: ft.Page):
    # 1. Instanciar el modelo puro
    engine = StudentEngine(sort_by="apellido")

    # 2. Cargar datos de prueba iniciales
    engine.seed_sample_data()

    # 3. Instanciar el controlador MVC
    controller = AppController(engine=engine)

    # 4. Iniciar la vista de escritorio conectada al controlador
    DesktopView(page=page, controller=controller)


def start():
    """Lanzador compatible multiplataforma (Win32 y Web)."""
    web = any(a in sys.argv for a in ("--web", "-w", "--browser"))
    if hasattr(ft, "run"):
        if web:
            print("[INFO] Iniciando servidor Web Flet: http://localhost:8550")
            ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)
        else:
            ft.run(main)
    elif hasattr(ft, "app"):
        if web:
            ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
        else:
            ft.app(target=main)
    else:
        raise RuntimeError("No se encontró el método de inicio de Flet (run / app).")


if __name__ == "__main__":
    start()
