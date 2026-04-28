"""
utils.py — Utilidades generales del Sistema POS
================================================
Este módulo agrupa funciones de apoyo que se reutilizan
en todos los demás módulos del sistema.

Funciones disponibles:
    - limpiar_pantalla : borra el contenido de la terminal
    - pausar           : detiene el programa hasta que el usuario presione Enter
    - separador        : imprime una línea decorativa
    - pedir_entero     : solicita y valida un número entero
    - pedir_flotante   : solicita y valida un número decimal
    - pedir_texto      : solicita y valida una cadena de texto no vacía
"""

import os


def limpiar_pantalla():
    """
    Borra el contenido visible de la terminal.

    Detecta automáticamente el sistema operativo:
    - Windows : ejecuta el comando 'cls'
    - Linux/Mac: ejecuta el comando 'clear'

    Ejemplo:
        >>> limpiar_pantalla()
        # La terminal queda en blanco
    """
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """
    Detiene la ejecución del programa hasta que el usuario presione Enter.

    Se usa para que el usuario pueda leer un mensaje antes de que
    la pantalla se limpie o cambie de sección.

    Ejemplo:
        >>> pausar()
        Presiona Enter para continuar...
    """
    input("\nPresiona Enter para continuar...")


def separador(caracter="-", largo=55):
    """
    Imprime una línea horizontal decorativa en la terminal.

    Se utiliza para dividir visualmente las secciones del menú
    y hacer la interfaz más legible.

    Parámetros:
        caracter (str): El carácter con el que se forma la línea.
                        Por defecto es "-".
        largo    (int): Número de veces que se repite el carácter.
                        Por defecto es 55.

    Ejemplo:
        >>> separador()
        -------------------------------------------------------
        >>> separador("=", 30)
        ==============================
    """
    print(caracter * largo)


def pedir_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita al usuario que ingrese un número entero y lo valida.

    Repite la solicitud en un bucle hasta recibir un valor válido.
    Verifica que sea un número entero y que esté dentro del rango
    indicado por 'minimo' y 'maximo' (si se proporcionan).

    Parámetros:
        mensaje (str): Texto que se muestra al usuario como instrucción.
        minimo  (int): Valor mínimo aceptado. None significa sin límite inferior.
        maximo  (int): Valor máximo aceptado. None significa sin límite superior.

    Retorna:
        int: El número entero ingresado por el usuario dentro del rango válido.

    Ejemplo:
        >>> cantidad = pedir_entero("Cantidad: ", minimo=1)
        Cantidad: abc
          Por favor ingresa un número entero válido.
        Cantidad: 0
          El valor debe ser al menos 1.
        Cantidad: 3
        >>> print(cantidad)
        3
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
    Solicita al usuario que ingrese un número decimal y lo valida.

    Repite la solicitud en un bucle hasta recibir un valor válido.
    Acepta números con punto decimal (por ejemplo: 25.50).

    Parámetros:
        mensaje (str)  : Texto que se muestra al usuario como instrucción.
        minimo  (float): Valor mínimo aceptado. Por defecto es 0.0.

    Retorna:
        float: El número decimal ingresado por el usuario.

    Ejemplo:
        >>> precio = pedir_flotante("Precio: $", minimo=0.01)
        Precio: $-5
          El valor debe ser mayor o igual a 0.01.
        Precio: $19.99
        >>> print(precio)
        19.99
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
    Solicita al usuario que ingrese una cadena de texto no vacía.

    Repite la solicitud en un bucle si el usuario presiona Enter
    sin escribir nada o ingresa solo espacios.

    Parámetros:
        mensaje (str): Texto que se muestra al usuario como instrucción.

    Retorna:
        str: La cadena de texto ingresada, sin espacios al inicio o al final.

    Ejemplo:
        >>> nombre = pedir_texto("Nombre del producto: ")
        Nombre del producto:
          Este campo no puede estar vacío.
        Nombre del producto: Coca-Cola 600ml
        >>> print(nombre)
        'Coca-Cola 600ml'
    """
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  Este campo no puede estar vacío.")
