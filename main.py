"""
main.py — Punto de entrada del Sistema POS
==========================================
Este es el archivo principal del Sistema POS (Punto de Venta).
Aquí se define el menú principal, los submenús y el flujo general
del programa. Para ejecutar el sistema, corre este archivo:

    python main.py

Arquitectura del proyecto:
    utils.py     → funciones auxiliares y validaciones de entrada
    productos.py → gestión del catálogo (agregar, buscar, mostrar)
    ventas.py    → carrito de compra y cálculo de totales
    ticket.py    → generación de tickets e historial de ventas
    main.py      → menús, navegación y flujo del programa (este archivo)

Carpeta de datos (se crea automáticamente):
    datos/catalogo.json          → productos del catálogo
    datos/historial_ventas.json  → registro de ventas completadas

Flujo general del programa:
    main()
    ├── proceso_venta()   → nueva venta completa
    ├── mostrar_catalogo()
    ├── agregar_producto()
    └── menu_historial()
        ├── mostrar_historial()
        └── mostrar_detalle_venta()
"""

from utils import limpiar_pantalla, pausar, separador, pedir_entero

from productos import (
    cargar_catalogo,
    mostrar_catalogo,
    agregar_producto,
    actualizar_stock,
)

from ventas import (
    iniciar_carrito,
    agregar_al_carrito,
    eliminar_del_carrito,
    mostrar_carrito,
    vaciar_carrito,
)

from ticket import (
    generar_ticket,
    guardar_venta,
    obtener_numero_venta,
    mostrar_historial,
    mostrar_detalle_venta,
)


# ---------------------------------------------------------------------------
# Menús
# ---------------------------------------------------------------------------

def mostrar_menu_principal():
    """
    Imprime el menú principal del sistema y solicita una opción al usuario.

    Muestra las cinco opciones disponibles:
        1. Nueva venta
        2. Ver catálogo de productos
        3. Agregar producto al catálogo
        4. Historial de ventas
        5. Salir

    Retorna:
        str: La opción ingresada por el usuario como cadena de texto.
             (Se usa str para comparar con "1", "2", etc.)
    """
    separador("=")
    print("        SISTEMA POS — MENÚ PRINCIPAL")
    separador("=")
    print("  1. Nueva venta")
    print("  2. Ver catálogo de productos")
    print("  3. Agregar producto al catálogo")
    print("  4. Historial de ventas")
    print("  5. Salir")
    separador("=")
    return input("  Selecciona una opción: ").strip()


def mostrar_menu_venta():
    """
    Imprime el menú de opciones durante una venta activa y solicita una opción.

    Muestra las cinco acciones disponibles dentro de una venta:
        1. Agregar producto al carrito
        2. Eliminar producto del carrito
        3. Ver carrito
        4. Finalizar venta (genera el ticket)
        5. Cancelar venta

    Retorna:
        str: La opción ingresada por el usuario como cadena de texto.
    """
    separador("-")
    print("  MENÚ DE VENTA")
    separador("-")
    print("  1. Agregar producto al carrito")
    print("  2. Eliminar producto del carrito")
    print("  3. Ver carrito")
    print("  4. Finalizar venta")
    print("  5. Cancelar venta")
    separador("-")
    return input("  Selecciona una opción: ").strip()


def mostrar_menu_historial():
    """
    Imprime el submenú de historial de ventas y solicita una opción.

    Muestra tres opciones:
        1. Ver resumen de todas las ventas
        2. Ver detalle completo de una venta específica
        3. Regresar al menú principal

    Retorna:
        str: La opción ingresada por el usuario como cadena de texto.
    """
    separador("-")
    print("  HISTORIAL DE VENTAS")
    separador("-")
    print("  1. Ver resumen de ventas")
    print("  2. Ver detalle de una venta")
    print("  3. Regresar al menú principal")
    separador("-")
    return input("  Selecciona una opción: ").strip()


# ---------------------------------------------------------------------------
# Flujo de venta
# ---------------------------------------------------------------------------

def proceso_venta(catalogo, numero_venta):
    """
    Ejecuta el ciclo completo de una venta desde el carrito hasta el ticket.

    Mantiene al usuario en un bucle donde puede agregar o eliminar
    productos, revisar el carrito y finalmente confirmar o cancelar la venta.

    Al confirmar:
        - Genera e imprime el ticket.
        - Descuenta el stock de cada producto vendido.
        - Guarda la venta en el historial.

    Al cancelar:
        - Vacía el carrito sin registrar ningún movimiento.

    Parámetros:
        catalogo     (dict): Diccionario del catálogo de productos disponibles.
        numero_venta (int) : Número correlativo asignado a esta venta.

    Retorna:
        bool: True si la venta se completó y confirmó exitosamente.
              False si el usuario canceló la venta.

    Ejemplo:
        >>> resultado = proceso_venta(catalogo, 1)
        # El usuario navega el menú de venta...
        >>> print(resultado)
        True  # si confirmó, False si canceló
    """
    carrito = iniciar_carrito()

    while True:
        limpiar_pantalla()
        print(f"\n  Venta #{numero_venta:04d}  |  Productos en carrito: {len(carrito)}")
        opcion = mostrar_menu_venta()

        # --- Agregar producto ---
        if opcion == "1":
            limpiar_pantalla()
            mostrar_catalogo(catalogo)
            codigo   = input("  Código del producto: ").strip()
            cantidad = pedir_entero("  Cantidad: ", minimo=1)
            agregar_al_carrito(carrito, catalogo, codigo, cantidad)
            pausar()

        # --- Eliminar producto ---
        elif opcion == "2":
            limpiar_pantalla()
            eliminar_del_carrito(carrito)
            pausar()

        # --- Ver carrito ---
        elif opcion == "3":
            limpiar_pantalla()
            mostrar_carrito(carrito)
            pausar()

        # --- Finalizar venta ---
        elif opcion == "4":
            if not carrito:
                print("\n  El carrito está vacío. Agrega al menos un producto.")
                pausar()
                continue

            limpiar_pantalla()
            generar_ticket(carrito, numero_venta)

            confirmar = input("\n  ¿Confirmar venta? (s/n): ").strip().lower()

            if confirmar == "s":
                for item in carrito:
                    actualizar_stock(catalogo, item["codigo"], item["cantidad"])
                guardar_venta(carrito, numero_venta)
                print("\n  Venta registrada exitosamente. ¡Gracias!")
                pausar()
                return True
            else:
                print("\n  Venta no confirmada. Puedes seguir editando el carrito.")
                pausar()

        # --- Cancelar venta ---
        elif opcion == "5":
            confirmar = input("\n  ¿Seguro que deseas cancelar la venta? (s/n): ").strip().lower()
            if confirmar == "s":
                vaciar_carrito(carrito)
                print("\n  Venta cancelada.")
                pausar()
                return False

        else:
            print("\n  Opción no válida. Intenta de nuevo.")
            pausar()


# ---------------------------------------------------------------------------
# Submenú de historial
# ---------------------------------------------------------------------------

def menu_historial():
    """
    Muestra el submenú de historial y gestiona la navegación dentro de él.

    Mantiene al usuario en un bucle hasta que elija regresar
    al menú principal. Desde aquí puede ver el resumen de todas
    las ventas o el detalle de una venta específica.
    """
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_historial()

        if opcion == "1":
            limpiar_pantalla()
            mostrar_historial()
            pausar()

        elif opcion == "2":
            limpiar_pantalla()
            mostrar_detalle_venta()
            pausar()

        elif opcion == "3":
            break  # Regresar al menú principal

        else:
            print("\n  Opción no válida.")
            pausar()


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    """
    Función principal del Sistema POS.

    Carga el catálogo de productos y el número de la próxima venta
    al iniciar. Luego entra en el bucle del menú principal donde
    el usuario navega entre las distintas funciones del sistema.

    El programa termina cuando el usuario selecciona la opción 5 (Salir).
    """
    catalogo     = cargar_catalogo()
    numero_venta = obtener_numero_venta()

    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_principal()

        # --- Nueva venta ---
        if opcion == "1":
            venta_completada = proceso_venta(catalogo, numero_venta)
            if venta_completada:
                numero_venta += 1  # Incrementar solo si la venta se confirmó

        # --- Ver catálogo ---
        elif opcion == "2":
            limpiar_pantalla()
            mostrar_catalogo(catalogo)
            pausar()

        # --- Agregar producto ---
        elif opcion == "3":
            limpiar_pantalla()
            agregar_producto(catalogo)
            pausar()

        # --- Historial de ventas ---
        elif opcion == "4":
            menu_historial()

        # --- Salir ---
        elif opcion == "5":
            limpiar_pantalla()
            print("\n  Cerrando el sistema... ¡Hasta luego!\n")
            break

        else:
            print("\n  Opción no válida. Por favor elige entre 1 y 5.")
            pausar()


# Este bloque asegura que main() solo se ejecute cuando se corre
# este archivo directamente, no cuando se importa desde otro módulo.
if __name__ == "__main__":
    main()
