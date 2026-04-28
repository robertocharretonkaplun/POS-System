"""
Sistema POS (Punto de Venta) en Python.
Proyecto integrador — Curso de Programación en Python (Nivel Básico-Intermedio).

Módulos:
  - utils.py     : funciones auxiliares y validaciones
  - productos.py : gestión del catálogo
  - ventas.py    : carrito de compra y cálculos
  - ticket.py    : generación de tickets e historial
  - main.py      : menú principal y flujo del programa (este archivo)

Cómo ejecutar:
  python main.py
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
    Ejecuta el flujo completo de una venta:
    agregar productos, revisar carrito, confirmar y generar ticket.

    Devuelve True si la venta se completó, False si se canceló.
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
# Menú de historial
# ---------------------------------------------------------------------------

def menu_historial():
    """Submenú para consultar el historial de ventas."""
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
            break

        else:
            print("\n  Opción no válida.")
            pausar()


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    """Función principal: carga el catálogo y ejecuta el menú principal."""
    catalogo      = cargar_catalogo()
    numero_venta  = obtener_numero_venta()

    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_principal()

        # --- Nueva venta ---
        if opcion == "1":
            venta_completada = proceso_venta(catalogo, numero_venta)
            if venta_completada:
                numero_venta += 1

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

        # --- Historial ---
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


if __name__ == "__main__":
    main()
