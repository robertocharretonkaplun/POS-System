"""
ventas.py — Gestión del carrito de compra
==========================================
Este módulo controla todo lo relacionado con el proceso de venta:
crear el carrito, agregar o eliminar productos, mostrar su contenido
y calcular los montos a cobrar.

El carrito se representa como una lista de diccionarios donde
cada elemento es un producto seleccionado por el cliente:
    [
        {
            "codigo"  : "A001",
            "nombre"  : "Coca-Cola 600ml",
            "precio"  : 20.0,
            "cantidad": 2,
            "subtotal": 40.0
        },
        ...
    ]

Constantes:
    TASA_IVA (float): Porcentaje del IVA aplicado al subtotal (0.16 = 16%).

Funciones disponibles:
    - iniciar_carrito      : crea un carrito vacío
    - agregar_al_carrito   : agrega o actualiza un producto en el carrito
    - eliminar_del_carrito : elimina un producto del carrito por número
    - mostrar_carrito      : imprime el contenido del carrito en pantalla
    - calcular_totales     : calcula subtotal, IVA y total
    - vaciar_carrito       : elimina todos los productos del carrito
"""

from utils import separador
from productos import buscar_producto


# Tasa del Impuesto al Valor Agregado (IVA) en México
TASA_IVA = 0.16  # 16%


def iniciar_carrito():
    """
    Crea y devuelve un carrito de compra vacío.

    El carrito es una lista de Python. Cada elemento que se agregue
    será un diccionario con los datos del producto seleccionado.

    Retorna:
        list: Lista vacía que representa un carrito sin productos.

    Ejemplo:
        >>> carrito = iniciar_carrito()
        >>> print(carrito)
        []
    """
    return []


def agregar_al_carrito(carrito, catalogo, codigo, cantidad):
    """
    Agrega un producto al carrito o incrementa su cantidad si ya existe.

    Antes de agregar, realiza dos validaciones:
        1. Verifica que el código exista en el catálogo.
        2. Verifica que haya suficiente stock disponible
           (considerando lo que ya está en el carrito).

    Si el producto ya estaba en el carrito, solo suma la cantidad
    y recalcula el subtotal. Si es nuevo, crea un nuevo elemento.

    Parámetros:
        carrito  (list): Lista del carrito donde se agregará el producto.
                         Se modifica directamente (in-place).
        catalogo (dict): Diccionario del catálogo para consultar el producto.
        codigo   (str) : Código del producto a agregar (ej. "A001").
        cantidad (int) : Número de unidades a agregar al carrito.

    Retorna:
        bool: True si el producto se agregó o actualizó correctamente.
              False si el código no existe o no hay suficiente stock.

    Ejemplo:
        >>> carrito = []
        >>> agregar_al_carrito(carrito, catalogo, "A001", 2)
          Agregado: Coca-Cola 600ml x2
        True
        >>> agregar_al_carrito(carrito, catalogo, "A001", 1)
          Cantidad actualizada: Coca-Cola 600ml x3
        True
    """
    producto = buscar_producto(catalogo, codigo)

    if producto is None:
        print(f"\n  El código '{codigo}' no existe en el catálogo.")
        return False

    # Calcular cuántas unidades ya están en el carrito para este producto
    cantidad_en_carrito = 0
    for item in carrito:
        if item["codigo"] == codigo.upper():
            cantidad_en_carrito = item["cantidad"]
            break

    if producto["stock"] < cantidad_en_carrito + cantidad:
        disponible = producto["stock"] - cantidad_en_carrito
        print(f"\n  Stock insuficiente. Puedes agregar hasta {disponible} unidad(es).")
        return False

    # Si el producto ya está en el carrito, actualizar la cantidad
    for item in carrito:
        if item["codigo"] == codigo.upper():
            item["cantidad"] += cantidad
            item["subtotal"] = item["precio"] * item["cantidad"]
            print(f"\n  Cantidad actualizada: {item['nombre']} x{item['cantidad']}")
            return True

    # Si el producto no está en el carrito, crear un nuevo elemento
    nuevo_item = {
        "codigo":   codigo.upper(),
        "nombre":   producto["nombre"],
        "precio":   producto["precio"],
        "cantidad": cantidad,
        "subtotal": producto["precio"] * cantidad,
    }
    carrito.append(nuevo_item)
    print(f"\n  Agregado: {producto['nombre']} x{cantidad}")
    return True


def eliminar_del_carrito(carrito):
    """
    Permite al usuario seleccionar y eliminar un producto del carrito.

    Muestra el carrito numerado y solicita al usuario el número
    del producto que desea quitar. Ingresando 0 se cancela la operación.

    Parámetros:
        carrito (list): Lista del carrito a modificar (in-place).

    Ejemplo:
        >>> # El carrito tiene: 1. Coca-Cola, 2. Sabritas
        >>> eliminar_del_carrito(carrito)
          Número del producto a eliminar (0 para cancelar): 1
          'Coca-Cola 600ml' eliminado del carrito.
    """
    if not carrito:
        print("\n  El carrito está vacío.")
        return

    mostrar_carrito(carrito)
    numero = input("  Número del producto a eliminar (0 para cancelar): ").strip()

    if numero == "0":
        return

    try:
        indice = int(numero) - 1
        if 0 <= indice < len(carrito):
            nombre = carrito[indice]["nombre"]
            carrito.pop(indice)
            print(f"\n  '{nombre}' eliminado del carrito.")
        else:
            print("\n  Número fuera de rango.")
    except ValueError:
        print("\n  Entrada no válida.")


def mostrar_carrito(carrito):
    """
    Imprime en pantalla el contenido actual del carrito de compra.

    Muestra una tabla con: número de línea, nombre del producto,
    precio unitario, cantidad y subtotal por producto.
    Si el carrito está vacío, muestra un mensaje informativo.

    Parámetros:
        carrito (list): Lista con los productos del carrito a mostrar.

    Ejemplo de salida:
        =======================================================
                   CARRITO DE COMPRA
        =======================================================
          #    Producto                    Precio   Cant   Subtotal
        -------------------------------------------------------
          1    Coca-Cola 600ml             $20.00      2     $40.00
          2    Sabritas Original           $18.00      1     $18.00
        -------------------------------------------------------
    """
    separador("=")
    print("           CARRITO DE COMPRA")
    separador("=")

    if not carrito:
        print("  El carrito está vacío.")
    else:
        print(f"  {'#':<4} {'Producto':<26} {'Precio':>10} {'Cant':>5} {'Subtotal':>10}")
        separador()
        for i, item in enumerate(carrito, start=1):
            print(
                f"  {i:<4} {item['nombre']:<26} "
                f"${item['precio']:>9.2f} {item['cantidad']:>4} "
                f"${item['subtotal']:>9.2f}"
            )

    separador()


def calcular_totales(carrito):
    """
    Calcula el subtotal, el IVA y el total de la venta.

    Suma los subtotales de todos los productos del carrito para
    obtener el subtotal. Luego aplica la tasa de IVA (16%) y
    suma ambos para obtener el total a pagar.

    Parámetros:
        carrito (list): Lista con los productos del carrito.
                        Cada elemento debe tener la llave 'subtotal'.

    Retorna:
        tuple: Una tupla con tres valores flotantes:
               (subtotal, iva, total)
               - subtotal : suma de todos los subtotales
               - iva      : subtotal * TASA_IVA (16%)
               - total    : subtotal + iva

    Ejemplo:
        >>> carrito = [{"subtotal": 40.0}, {"subtotal": 18.0}]
        >>> subtotal, iva, total = calcular_totales(carrito)
        >>> print(subtotal, iva, total)
        58.0  9.28  67.28
    """
    subtotal = sum(item["subtotal"] for item in carrito)
    iva      = subtotal * TASA_IVA
    total    = subtotal + iva
    return subtotal, iva, total


def vaciar_carrito(carrito):
    """
    Elimina todos los productos del carrito.

    Se llama cuando el usuario cancela una venta para dejar
    el carrito limpio. Modifica la lista directamente (in-place)
    usando el método .clear().

    Parámetros:
        carrito (list): Lista del carrito a vaciar.

    Ejemplo:
        >>> carrito = [{"nombre": "Coca-Cola"}, {"nombre": "Sabritas"}]
        >>> vaciar_carrito(carrito)
        >>> print(carrito)
        []
    """
    carrito.clear()
