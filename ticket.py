"""
ticket.py — Generación de tickets e historial de ventas
========================================================
Este módulo se encarga de dos responsabilidades:

1. Generar el ticket de venta: imprime en pantalla un recibo
   con el detalle de los productos, subtotal, IVA y total.

2. Gestionar el historial: guarda cada venta completada en un
   archivo JSON y permite consultarlas posteriormente.

Cada venta guardada en el historial tiene esta estructura:
    {
        "numero"   : 1,
        "fecha"    : "27/04/2026 10:35:22",
        "productos": [ {...}, {...} ],
        "subtotal" : 58.00,
        "iva"      : 9.28,
        "total"    : 67.28
    }

Funciones disponibles:
    - cargar_historial      : lee el historial desde el archivo JSON
    - guardar_venta         : agrega una venta al historial y lo guarda
    - obtener_numero_venta  : determina el número correlativo de la siguiente venta
    - generar_ticket        : imprime el ticket de venta en pantalla
    - mostrar_historial     : muestra un resumen de todas las ventas
    - mostrar_detalle_venta : muestra el detalle completo de una venta
"""

import json
import os
from datetime import datetime

from utils import separador
from ventas import calcular_totales


# Ruta del archivo donde se guarda el historial de ventas
ARCHIVO_HISTORIAL = os.path.join("datos", "historial_ventas.json")


# ---------------------------------------------------------------------------
# Historial
# ---------------------------------------------------------------------------

def cargar_historial():
    """
    Carga la lista de ventas registradas desde el archivo JSON.

    Si el archivo no existe (no se ha completado ninguna venta aún),
    devuelve una lista vacía en lugar de producir un error.

    Retorna:
        list: Lista de diccionarios, donde cada elemento es una venta.
              Devuelve una lista vacía si no hay ventas registradas.

    Ejemplo:
        >>> historial = cargar_historial()
        >>> print(len(historial))
        3   # si hay 3 ventas guardadas
    """
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []


def guardar_venta(carrito, numero_venta):
    """
    Registra la venta actual en el historial y guarda el archivo JSON.

    Construye un diccionario con todos los datos de la venta
    (número, fecha, productos, montos) y lo agrega al historial existente.
    Crea la carpeta 'datos/' automáticamente si no existe.

    Parámetros:
        carrito      (list): Lista con los productos de la venta a guardar.
        numero_venta (int) : Número correlativo que identifica esta venta.

    Ejemplo:
        >>> guardar_venta(carrito, 1)
        # Se agrega la venta al archivo datos/historial_ventas.json
    """
    subtotal, iva, total = calcular_totales(carrito)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    venta = {
        "numero":    numero_venta,
        "fecha":     fecha_hora,
        "productos": [item.copy() for item in carrito],  # copia para no alterar el original
        "subtotal":  round(subtotal, 2),
        "iva":       round(iva, 2),
        "total":     round(total, 2),
    }

    historial = cargar_historial()
    historial.append(venta)

    os.makedirs("datos", exist_ok=True)
    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)


def obtener_numero_venta():
    """
    Determina el número correlativo de la próxima venta.

    Lee el historial y toma el número de la última venta registrada,
    luego le suma 1. Si no hay ventas previas, devuelve 1.

    Este mecanismo permite que el contador de ventas persista
    entre ejecuciones del programa.

    Retorna:
        int: Número que le corresponde a la siguiente venta.

    Ejemplo:
        >>> # Si la última venta fue la #5
        >>> numero = obtener_numero_venta()
        >>> print(numero)
        6
    """
    historial = cargar_historial()
    if historial:
        return historial[-1]["numero"] + 1
    return 1


# ---------------------------------------------------------------------------
# Ticket en pantalla
# ---------------------------------------------------------------------------

def generar_ticket(carrito, numero_venta):
    """
    Imprime el ticket de venta en pantalla con formato de recibo.

    Muestra el número de venta, la fecha y hora actuales, el detalle
    de cada producto (cantidad, precio unitario y subtotal), y al final
    el subtotal, el IVA (16%) y el total a pagar.

    Parámetros:
        carrito      (list): Lista con los productos de la venta.
        numero_venta (int) : Número correlativo de esta venta.

    Retorna:
        tuple: Una tupla con tres flotantes: (subtotal, iva, total).
               Se retorna por si se necesita usar los montos después
               de mostrar el ticket.

    Ejemplo de salida:
        =======================================================
                 SISTEMA POS — TICKET DE VENTA
        =======================================================
          Venta  : #0001
          Fecha  : 27/04/2026  10:35:22
        -------------------------------------------------------
          Producto                   Cant    P.Unit   Subtotal
        -------------------------------------------------------
          Coca-Cola 600ml               2    $20.00     $40.00
        -------------------------------------------------------
          Subtotal:                              $40.00
          IVA (16%):                              $6.40
        -------------------------------------------------------
          TOTAL A PAGAR:                         $46.40
        =======================================================
    """
    subtotal, iva, total = calcular_totales(carrito)
    fecha_hora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    separador("=")
    print("         SISTEMA POS — TICKET DE VENTA")
    separador("=")
    print(f"  Venta  : #{numero_venta:04d}")
    print(f"  Fecha  : {fecha_hora}")
    separador()
    print(f"  {'Producto':<26} {'Cant':>4} {'P.Unit':>9} {'Subtotal':>10}")
    separador()

    for item in carrito:
        print(
            f"  {item['nombre']:<26} {item['cantidad']:>4} "
            f"${item['precio']:>8.2f} ${item['subtotal']:>9.2f}"
        )

    separador()
    print(f"  {'Subtotal:':<38} ${subtotal:>9.2f}")
    print(f"  {'IVA (16%):':<38} ${iva:>9.2f}")
    separador()
    print(f"  {'TOTAL A PAGAR:':<38} ${total:>9.2f}")
    separador("=")

    return subtotal, iva, total


# ---------------------------------------------------------------------------
# Historial en pantalla
# ---------------------------------------------------------------------------

def mostrar_historial():
    """
    Imprime en pantalla un resumen de todas las ventas registradas.

    Muestra una tabla con: número de venta, fecha, cantidad total
    de productos vendidos y el monto total cobrado.
    Si no hay ventas, muestra un mensaje informativo.

    Ejemplo de salida:
        =======================================================
                   HISTORIAL DE VENTAS
        =======================================================
          #      Fecha                Productos        Total
        -------------------------------------------------------
          #1     27/04/2026 10:35:22         3       $67.28
    """
    historial = cargar_historial()

    separador("=")
    print("           HISTORIAL DE VENTAS")
    separador("=")

    if not historial:
        print("  No hay ventas registradas.")
    else:
        print(f"  {'#':<6} {'Fecha':<20} {'Productos':>9} {'Total':>12}")
        separador()
        for venta in historial:
            num_productos = sum(p["cantidad"] for p in venta["productos"])
            print(
                f"  #{venta['numero']:<5} {venta['fecha']:<20} "
                f"{num_productos:>8} ${venta['total']:>11.2f}"
            )

    separador()


def mostrar_detalle_venta():
    """
    Muestra el detalle completo de una venta seleccionada por el usuario.

    Primero imprime el historial general para que el usuario identifique
    el número de venta que desea consultar. Luego busca esa venta y
    muestra todos sus datos: productos, cantidades, precios y totales.

    Si el número ingresado no corresponde a ninguna venta, muestra
    un mensaje de error. Ingresar 0 cancela la operación.

    Ejemplo de salida:
        =======================================================
          DETALLE — VENTA #0001
        =======================================================
          Fecha: 27/04/2026 10:35:22
        -------------------------------------------------------
          Coca-Cola 600ml          2   $20.00     $40.00
          Sabritas Original        1   $18.00     $18.00
        -------------------------------------------------------
          Subtotal:                              $58.00
          IVA (16%):                              $9.28
        -------------------------------------------------------
          TOTAL:                                 $67.28
        =======================================================
    """
    historial = cargar_historial()

    if not historial:
        print("\n  No hay ventas registradas.")
        return

    mostrar_historial()
    numero = input("  Ingresa el número de venta a consultar (0 para cancelar): ").strip()

    if numero == "0":
        return

    try:
        numero = int(numero)
    except ValueError:
        print("\n  Entrada no válida.")
        return

    # Buscar la venta cuyo número coincida con el ingresado
    venta = next((v for v in historial if v["numero"] == numero), None)

    if venta is None:
        print(f"\n  No se encontró la venta #{numero}.")
        return

    separador("=")
    print(f"  DETALLE — VENTA #{venta['numero']:04d}")
    separador("=")
    print(f"  Fecha: {venta['fecha']}")
    separador()
    print(f"  {'Producto':<26} {'Cant':>4} {'P.Unit':>9} {'Subtotal':>10}")
    separador()

    for item in venta["productos"]:
        print(
            f"  {item['nombre']:<26} {item['cantidad']:>4} "
            f"${item['precio']:>8.2f} ${item['subtotal']:>9.2f}"
        )

    separador()
    print(f"  {'Subtotal:':<38} ${venta['subtotal']:>9.2f}")
    print(f"  {'IVA (16%):':<38} ${venta['iva']:>9.2f}")
    separador()
    print(f"  {'TOTAL:':<38} ${venta['total']:>9.2f}")
    separador("=")
