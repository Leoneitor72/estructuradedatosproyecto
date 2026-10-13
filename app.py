"""Punto de entrada de la Aplicación de Escritorio Flet (Semana 2 - Día 5).
Ejecuta la interfaz nativa en Windows (Win32), macOS o Linux.
Compatible tanto con Flet 1.x (ft.run) como con Flet 0.x (ft.app).
"""

import flet as ft
from models.student_engine import StudentEngine
from controllers.app_controller import AppController
from views.desktop_view import DesktopView


def main(page: ft.Page):
    # 1. Instanciar el modelo puro
    engine = StudentEngine(sort_by="apellido")

    # 2. Cargar datos de prueba iniciales para que la interfaz se vea viva de inmediato
    engine.seed_sample_data()

    # 3. Instanciar el controlador MVC
    controller = AppController(engine=engine)

    # 4. Iniciar la vista de escritorio conectada al controlador
    DesktopView(page=page, controller=controller)


def start():
    """Lanzador compatible multiplataforma."""
    if hasattr(ft, "run"):
        ft.run(main)
    elif hasattr(ft, "app"):
        ft.app(target=main)
    else:
        raise RuntimeError("No se encontró el método de inicio de Flet (run / app).")


if __name__ == "__main__":
    start()
