"""
Módulo de gestión de productos del Sistema POS.
Permite cargar, guardar, mostrar, buscar y agregar
productos en el catálogo.
"""

import json
import os

from utils import pedir_texto, pedir_flotante, pedir_entero, separador


ARCHIVO_CATALOGO = os.path.join("datos", "catalogo.json")

# Catálogo inicial que se usa si no existe el archivo de datos
CATALOGO_INICIAL = {
    "A001": {"nombre": "Coca-Cola 600ml",      "precio": 20.00, "stock": 50},
    "A002": {"nombre": "Agua Mineral 1L",       "precio": 15.00, "stock": 40},
    "A003": {"nombre": "Jugo del Valle 1L",     "precio": 22.00, "stock": 35},
    "B001": {"nombre": "Sabritas Original",     "precio": 18.00, "stock": 30},
    "B002": {"nombre": "Doritos Nacho",         "precio": 20.00, "stock": 25},
    "C001": {"nombre": "Pan Bimbo Blanco",      "precio": 35.00, "stock": 20},
    "C002": {"nombre": "Leche Lala Entera 1L",  "precio": 28.00, "stock": 25},
    "C003": {"nombre": "Huevo Blanco 12 pzas",  "precio": 45.00, "stock": 15},
}


def cargar_catalogo():
    """
    Carga el catálogo desde el archivo JSON.
    Si el archivo no existe, devuelve el catálogo inicial.
    """
    if os.path.exists(ARCHIVO_CATALOGO):
        with open(ARCHIVO_CATALOGO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return CATALOGO_INICIAL.copy()


def guardar_catalogo(catalogo):
    """Guarda el catálogo actual en el archivo JSON."""
    os.makedirs("datos", exist_ok=True)
    with open(ARCHIVO_CATALOGO, "w", encoding="utf-8") as archivo:
        json.dump(catalogo, archivo, indent=4, ensure_ascii=False)


def mostrar_catalogo(catalogo):
    """Imprime en pantalla todos los productos del catálogo."""
    separador("=")
    print("           CATÁLOGO DE PRODUCTOS")
    separador("=")

    if not catalogo:
        print("  No hay productos registrados.")
    else:
        print(f"  {'Código':<8} {'Nombre':<26} {'Precio':>10} {'Stock':>7}")
        separador()
        for codigo, producto in catalogo.items():
            print(
                f"  {codigo:<8} {producto['nombre']:<26} "
                f"${producto['precio']:>9.2f} {producto['stock']:>6}"
            )

    separador()


def buscar_producto(catalogo, codigo):
    """
    Busca un producto por su código.
    Devuelve el diccionario del producto o None si no existe.
    """
    return catalogo.get(codigo.upper())


def agregar_producto(catalogo):
    """
    Solicita los datos de un nuevo producto y lo agrega al catálogo.
    Valida que el código no esté duplicado.
    """
    separador("=")
    print("           AGREGAR NUEVO PRODUCTO")
    separador("=")

    codigo = pedir_texto("  Código del producto (ej. D001): ").upper()

    if codigo in catalogo:
        print(f"\n  El código '{codigo}' ya existe en el catálogo.")
        return

    nombre = pedir_texto("  Nombre del producto: ")
    precio = pedir_flotante("  Precio unitario: $", minimo=0.01)
    stock  = pedir_entero("  Stock inicial: ", minimo=0)

    catalogo[codigo] = {
        "nombre": nombre,
        "precio": precio,
        "stock":  stock,
    }

    guardar_catalogo(catalogo)
    print(f"\n  Producto '{nombre}' agregado correctamente.")


def actualizar_stock(catalogo, codigo, cantidad_vendida):
    """Descuenta del stock la cantidad vendida de un producto."""
    if codigo in catalogo:
        catalogo[codigo]["stock"] -= cantidad_vendida
        guardar_catalogo(catalogo)
