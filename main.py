"""Demostración del Sistema de Gestión de Estudiantes - Semana 1.
Ejecuta y valida el flujo completo de datos y estructuras manuales.
"""

from models.student_management import StudentManager
from models.student import Estudiante


def main():
    print("=" * 60)
    print(" SIMULADOR DE GESTION DE ESTUDIANTES - SEMANA 1")
    print(" Modelo y Estructuras de Datos Lineales Puras (Sin listas nativas)")
    print("=" * 60)

    # 1. Instanciación del gestor ordenado por apellido
    manager = StudentManager(sort_by="apellido")

    # 2. Funcionalidad 1: Inscribir Estudiantes
    print("\n[1] Inscribiendo Estudiantes...")
    manager.inscribir_estudiante("EST-101", "Maria", "Gonzalez", [18.5, 19.0, 17.0])
    manager.inscribir_estudiante("EST-102", "Alejandro", "Barrios", [14.0, 15.5, 13.0])
    manager.inscribir_estudiante("EST-103", "Camila", "Diaz", [20.0, 19.5, 19.0])
    manager.inscribir_estudiante("EST-104", "Esteban", "Torres", [11.0, 12.0, 10.5])
    print("[OK] 4 estudiantes inscritos correctamente.")

    # 3. Funcionalidad 5: Generar Reporte
    print("\n[2] Reporte Inicial (Ordenado por Apellido):")
    print(manager.generar_reporte_texto())

    # 4. Funcionalidad 4: Calcular Promedio
    id_calc = "EST-103"
    promedio = manager.calcular_promedio(id_calc)
    print(f"\n[3] Promedio calculado para {id_calc}: {promedio:.2f}")

    # 5. Funcionalidad 3: Actualizar Calificaciones
    print("\n[4] Actualizando calificaciones de EST-104...")
    manager.actualizar_calificaciones("EST-104", [16.0, 17.5, 18.0])
    print(f"[OK] Nuevo promedio de EST-104: {manager.calcular_promedio('EST-104'):.2f}")

    # 6. Funcionalidad 2: Dar de Baja a un Estudiante
    print("\n[5] Dando de baja al estudiante EST-102 (Alejandro Barrios)...")
    manager.dar_de_baja("EST-102")
    print(manager.generar_reporte_texto())

    # 7. Prueba del Gestor Undo / Redo mediante Doble Pila
    print("\n[6] Demostracion de Deshacer (Undo) mediante Pila:")
    msg_undo = manager.deshacer()
    print(f"<- Accion revertida: {msg_undo}")
    print("Reporte tras Deshacer:")
    print(manager.generar_reporte_texto())

    print("\n[7] Demostracion de Rehacer (Redo):")
    msg_redo = manager.rehacer()
    print(f"-> Accion repetida: {msg_redo}")
    print("Reporte tras Rehacer:")
    print(manager.generar_reporte_texto())

    # 8. Cola de Prioridad (Admisiones)
    print("\n[8] Cola de Prioridad para Solicitudes Especiales:")
    manager.encolar_solicitud_prioritaria(Estudiante("ESP-01", "Lucia", "Mendez"), prioridad=2.0)
    manager.encolar_solicitud_prioritaria(Estudiante("ESP-02", "Javier", "Paz (Beca Excelencia)"), prioridad=9.5)
    manager.encolar_solicitud_prioritaria(Estudiante("ESP-03", "Andres", "Ruiz (Reubicacion)"), prioridad=5.0)

    atendido = manager.atender_siguiente_solicitud()
    print(f"[OK] Solicitud de maxima prioridad atendida: {atendido.nombre} {atendido.apellido}")

    # 9. Cola Circular (Rondas de Turno)
    print("\n[9] Ronda Circular (Round-Robin) de Estudiantes:")
    manager.cargar_ronda_circular()
    print(f"Turno 1: {manager.siguiente_en_turno()}")
    print(f"Turno 2: {manager.siguiente_en_turno()}")

    print("\n" + "=" * 60)
    print(" [EXITO] Semana 1 completada al 100%! ")
    print("=" * 60)


if __name__ == "__main__":
    main()
