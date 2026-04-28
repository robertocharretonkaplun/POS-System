"""
Módulo de utilidades generales del Sistema POS.
Contiene funciones de uso común: limpieza de pantalla,
pausas, validaciones de entrada y separadores visuales.
"""

import os


def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresiona Enter para continuar...")


def separador(caracter="-", largo=55):
    """Imprime una línea decorativa de separación."""
    print(caracter * largo)


def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita un número entero al usuario con validación.
    Repite la solicitud hasta obtener un valor válido.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  El valor debe ser al menos {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  El valor debe ser máximo {maximo}.")
                continue
            return valor
        except ValueError:
            print("  Por favor ingresa un número entero válido.")


def pedir_flotante(mensaje, minimo=0.0):
    """
    Solicita un número decimal al usuario con validación.
    Repite la solicitud hasta obtener un valor válido.
    """
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                print(f"  El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Por favor ingresa un número válido (ejemplo: 25.50).")


def pedir_texto(mensaje):
    """
    Solicita una cadena de texto no vacía al usuario.
    Repite la solicitud si el campo queda en blanco.
    """
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  Este campo no puede estar vacío.")
