# Sistema POS en Python
### Proyecto Integrador — Curso de Programación en Python (Nivel Básico-Intermedio)

Este proyecto es el resultado del curso de programación en Python. Consiste en un **Sistema POS (Punto de Venta)** que funciona desde la terminal y permite registrar productos, realizar ventas y consultar el historial.

---

## Requisitos

- Python 3.8 o superior
- No se necesitan librerías externas (solo las que vienen con Python)

---

## Cómo ejecutar el proyecto

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta el archivo principal:

```
python main.py
```

---

## Estructura del proyecto

```
sistema_pos/
│
├── main.py          # Punto de entrada y menú principal
├── productos.py     # Gestión del catálogo de productos
├── ventas.py        # Carrito de compra y cálculos
├── ticket.py        # Generación de tickets e historial
├── utils.py         # Funciones auxiliares y validaciones
│
└── datos/
    ├── catalogo.json          # Se crea automáticamente al agregar productos
    └── historial_ventas.json  # Se crea automáticamente al registrar ventas
```

---

## Funcionalidades

| Función                        | Descripción                                          |
|-------------------------------|------------------------------------------------------|
| Nueva venta                   | Agrega productos al carrito y genera el ticket       |
| Ver catálogo                  | Lista todos los productos con precio y stock         |
| Agregar producto al catálogo  | Registra un nuevo producto con código, nombre y precio |
| Historial de ventas           | Consulta ventas anteriores con sus detalles          |

---

## Conceptos de Python aplicados

- Variables y tipos de datos (`str`, `int`, `float`, `bool`)
- Estructuras de control (`if`, `elif`, `else`, `while`, `for`)
- Estructuras de datos (`list`, `dict`)
- Funciones con parámetros y valores de retorno
- Módulos y organización del código en archivos
- Manejo de archivos JSON para persistencia de datos
- Validación de entradas del usuario

---

## Ejemplo de ticket generado

```
=======================================================
         SISTEMA POS — TICKET DE VENTA
=======================================================
  Venta  : #0001
  Fecha  : 27/04/2026  10:35:22
-------------------------------------------------------
  Producto                   Cant    P.Unit   Subtotal
-------------------------------------------------------
  Coca-Cola 600ml               2    $20.00     $40.00
  Sabritas Original             1    $18.00     $18.00
-------------------------------------------------------
  Subtotal:                              $58.00
  IVA (16%):                              $9.28
-------------------------------------------------------
  TOTAL A PAGAR:                         $67.28
=======================================================
```
