"""
Módulo de gestión de ventas del Sistema POS.
Controla el carrito de compra: agregar productos,
mostrar contenido y calcular totales.
"""

from utils import separador
from productos import buscar_producto


TASA_IVA = 0.16  # 16% de IVA


def iniciar_carrito():
    """Crea y devuelve un carrito de compra vacío (lista)."""
    return []


def agregar_al_carrito(carrito, catalogo, codigo, cantidad):
    """
    Agrega un producto al carrito o incrementa su cantidad si ya existe.

    Verifica que:
    - El código exista en el catálogo.
    - Haya suficiente stock disponible.

    Devuelve True si se agregó correctamente, False en caso contrario.
    """
    producto = buscar_producto(catalogo, codigo)

    if producto is None:
        print(f"\n  El código '{codigo}' no existe en el catálogo.")
        return False

    # Calcular cuántas unidades ya están en el carrito
    cantidad_en_carrito = 0
    for item in carrito:
        if item["codigo"] == codigo.upper():
            cantidad_en_carrito = item["cantidad"]
            break

    if producto["stock"] < cantidad_en_carrito + cantidad:
        disponible = producto["stock"] - cantidad_en_carrito
        print(f"\n  Stock insuficiente. Puedes agregar hasta {disponible} unidad(es).")
        return False

    # Si el producto ya está en el carrito, actualizar cantidad
    for item in carrito:
        if item["codigo"] == codigo.upper():
            item["cantidad"] += cantidad
            item["subtotal"] = item["precio"] * item["cantidad"]
            print(f"\n  Cantidad actualizada: {item['nombre']} x{item['cantidad']}")
            return True

    # Si es un producto nuevo, agregarlo al carrito
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
    Muestra el carrito y permite al usuario eliminar un producto por número.
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
    """Imprime en pantalla el contenido actual del carrito."""
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
    Calcula subtotal, IVA y total del carrito.
    Devuelve una tupla: (subtotal, iva, total).
    """
    subtotal = sum(item["subtotal"] for item in carrito)
    iva      = subtotal * TASA_IVA
    total    = subtotal + iva
    return subtotal, iva, total


def vaciar_carrito(carrito):
    """Elimina todos los productos del carrito."""
    carrito.clear()
