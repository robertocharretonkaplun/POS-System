"""
productos.py — Gestión del catálogo de productos
=================================================
Este módulo se encarga de todo lo relacionado con los productos:
cargar y guardar el catálogo, mostrarlo en pantalla, buscar
un producto por código y registrar nuevos productos.

El catálogo se representa como un diccionario donde:
    - La clave  es el código del producto (str), por ejemplo "A001".
    - El valor  es otro diccionario con las llaves:
        "nombre" (str)  : nombre del producto
        "precio" (float): precio unitario en pesos
        "stock"  (int)  : unidades disponibles en inventario

Ejemplo de estructura del catálogo:
    {
        "A001": {"nombre": "Coca-Cola 600ml", "precio": 20.0, "stock": 50},
        "B001": {"nombre": "Sabritas Original", "precio": 18.0, "stock": 30}
    }

Funciones disponibles:
    - cargar_catalogo    : carga productos desde archivo o usa el catálogo inicial
    - guardar_catalogo   : guarda el catálogo en disco como archivo JSON
    - mostrar_catalogo   : imprime el catálogo en forma de tabla
    - buscar_producto    : busca y devuelve un producto por su código
    - agregar_producto   : solicita datos y agrega un nuevo producto
    - actualizar_stock   : descuenta unidades vendidas del inventario
"""

import json
import os

from utils import pedir_texto, pedir_flotante, pedir_entero, separador


# Ruta del archivo donde se guarda el catálogo
ARCHIVO_CATALOGO = os.path.join("datos", "catalogo.json")

# Productos con los que inicia el sistema si no existe el archivo de datos
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
    Carga el catálogo de productos desde el archivo JSON.

    Si el archivo 'datos/catalogo.json' existe, lo lee y devuelve
    su contenido. Si no existe (primera vez que se ejecuta el sistema),
    devuelve una copia del catálogo inicial definido en este módulo.

    Retorna:
        dict: Diccionario con los productos del catálogo.
              Las claves son los códigos y los valores son
              diccionarios con 'nombre', 'precio' y 'stock'.

    Ejemplo:
        >>> catalogo = cargar_catalogo()
        >>> print(catalogo["A001"])
        {'nombre': 'Coca-Cola 600ml', 'precio': 20.0, 'stock': 50}
    """
    if os.path.exists(ARCHIVO_CATALOGO):
        with open(ARCHIVO_CATALOGO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return CATALOGO_INICIAL.copy()


def guardar_catalogo(catalogo):
    """
    Guarda el catálogo actual en el archivo JSON de datos.

    Crea la carpeta 'datos/' automáticamente si no existe.
    El archivo se escribe con formato legible (indent=4) y
    soporte para caracteres en español (ensure_ascii=False).

    Parámetros:
        catalogo (dict): Diccionario completo del catálogo a guardar.

    Ejemplo:
        >>> guardar_catalogo(catalogo)
        # Se crea o actualiza el archivo datos/catalogo.json
    """
    os.makedirs("datos", exist_ok=True)
    with open(ARCHIVO_CATALOGO, "w", encoding="utf-8") as archivo:
        json.dump(catalogo, archivo, indent=4, ensure_ascii=False)


def mostrar_catalogo(catalogo):
    """
    Imprime en pantalla todos los productos del catálogo en forma de tabla.

    Muestra columnas de: Código, Nombre, Precio y Stock.
    Si el catálogo está vacío, muestra un mensaje informativo.

    Parámetros:
        catalogo (dict): Diccionario con los productos a mostrar.

    Ejemplo de salida:
        =======================================================
                   CATÁLOGO DE PRODUCTOS
        =======================================================
          Código   Nombre                      Precio    Stock
        -------------------------------------------------------
          A001     Coca-Cola 600ml             $20.00       50
    """
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
    Busca un producto en el catálogo usando su código.

    Convierte el código a mayúsculas antes de buscarlo,
    por lo que la búsqueda no distingue entre mayúsculas y minúsculas.

    Parámetros:
        catalogo (dict): Diccionario completo del catálogo.
        codigo   (str) : Código del producto a buscar (ej. "a001" o "A001").

    Retorna:
        dict : Diccionario con los datos del producto si se encuentra.
               Contiene las llaves 'nombre', 'precio' y 'stock'.
        None : Si el código no existe en el catálogo.

    Ejemplo:
        >>> producto = buscar_producto(catalogo, "a001")
        >>> print(producto)
        {'nombre': 'Coca-Cola 600ml', 'precio': 20.0, 'stock': 50}

        >>> buscar_producto(catalogo, "Z999")
        None
    """
    return catalogo.get(codigo.upper())


def agregar_producto(catalogo):
    """
    Solicita al usuario los datos de un nuevo producto y lo agrega al catálogo.

    Pide los siguientes datos:
        - Código  : identificador único (se convierte a mayúsculas automáticamente)
        - Nombre  : descripción del producto
        - Precio  : valor unitario (debe ser mayor a $0.00)
        - Stock   : cantidad inicial en inventario (puede ser 0)

    Valida que el código no esté duplicado antes de agregar.
    Al finalizar, guarda el catálogo actualizado en el archivo JSON.

    Parámetros:
        catalogo (dict): Diccionario del catálogo donde se agregará el producto.
                         Se modifica directamente (in-place).

    Ejemplo:
        >>> agregar_producto(catalogo)
          Código del producto (ej. D001): D001
          Nombre del producto: Pepsi 600ml
          Precio unitario: $19.00
          Stock inicial: 40
          Producto 'Pepsi 600ml' agregado correctamente.
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
    """
    Descuenta del stock de un producto la cantidad que fue vendida.

    Se llama automáticamente al confirmar una venta para mantener
    el inventario actualizado. Si el código no existe, no hace nada.
    Guarda el catálogo en disco después de actualizar.

    Parámetros:
        catalogo        (dict): Diccionario del catálogo a actualizar.
        codigo          (str) : Código del producto cuyo stock se reducirá.
        cantidad_vendida (int): Número de unidades vendidas a descontar.

    Ejemplo:
        >>> # Antes: stock de A001 = 50
        >>> actualizar_stock(catalogo, "A001", 3)
        >>> # Después: stock de A001 = 47
    """
    if codigo in catalogo:
        catalogo[codigo]["stock"] -= cantidad_vendida
        guardar_catalogo(catalogo)
