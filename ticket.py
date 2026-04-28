"""
Módulo de tickets e historial de ventas del Sistema POS.
Genera el ticket en pantalla, guarda cada venta en un
archivo JSON y permite consultar el historial.
"""

import json
import os
from datetime import datetime

from utils import separador
from ventas import calcular_totales


ARCHIVO_HISTORIAL = os.path.join("datos", "historial_ventas.json")


# ---------------------------------------------------------------------------
# Historial
# ---------------------------------------------------------------------------

def cargar_historial():
    """Carga la lista de ventas desde el archivo JSON."""
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []


def guardar_venta(carrito, numero_venta):
    """Agrega la venta actual al historial y la escribe en disco."""
    subtotal, iva, total = calcular_totales(carrito)
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    venta = {
        "numero":    numero_venta,
        "fecha":     fecha_hora,
        "productos": [item.copy() for item in carrito],
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
    Determina el número de la próxima venta basándose en el historial.
    Si no hay ventas anteriores, comienza desde 1.
    """
    historial = cargar_historial()
    if historial:
        return historial[-1]["numero"] + 1
    return 1


# ---------------------------------------------------------------------------
# Ticket
# ---------------------------------------------------------------------------

def generar_ticket(carrito, numero_venta):
    """
    Imprime el ticket de venta en pantalla.
    Devuelve la tupla (subtotal, iva, total).
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
    """Imprime un resumen de todas las ventas registradas."""
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
    """Permite al usuario ver el detalle completo de una venta por número."""
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
