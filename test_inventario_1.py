# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 01:32:26 2024

@author: celes
"""
import tkinter as tk
from tkinter import messagebox, simpledialog

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("980x600")
ventana.title("Gestión de Inventario")
ventana.configure(bg="#ffe6f2")

# Listas para almacenar datos de productos
cantidad = []
productos = []
precio = []

# Función para añadir productos
def anadir_producto():
    ap = entry_producto.get()
    if not ap:
        messagebox.showerror("Error", "El nombre del producto es obligatorio.")
        return
    
    ac = entry_cantidad.get()
    apre = entry_precio.get()
    ac = int(ac) if ac else 0
    apre = int(apre) if apre else 0

    cantidad.append(ac)
    productos.append(ap)
    precio.append(apre)
    messagebox.showinfo("Éxito", f"Producto '{ap}' añadido con éxito.")
    limpiar_campos()

# Función para buscar y modificar productos
def buscar_producto():
    buscador = entry_producto.get()
    if buscador in productos:
        posicion = productos.index(buscador)

        # Crear una ventana emergente para modificar el producto
        ventana_modificar = tk.Toplevel(ventana)
        ventana_modificar.title(f"Modificar {buscador}")
        ventana_modificar.geometry("400x300")
        ventana_modificar.configure(bg="#ffe6f2")

        tk.Label(ventana_modificar, text="Modificar Producto", bg="#ffe6f2", fg="#8c008c", font=("Arial", 14, "bold")).pack(pady=10)

        # Mostrar valores actuales
        tk.Label(ventana_modificar, text=f"Producto actual: {productos[posicion]}", bg="#ffe6f2", fg="#660066", font=("Arial", 10)).pack()
        tk.Label(ventana_modificar, text=f"Cantidad actual: {cantidad[posicion]}", bg="#ffe6f2", fg="#660066", font=("Arial", 10)).pack()
        tk.Label(ventana_modificar, text=f"Precio actual: ${precio[posicion]}", bg="#ffe6f2", fg="#660066", font=("Arial", 10)).pack()

        # Entradas para modificar
        entry_nueva_cantidad = tk.Entry(ventana_modificar, bg="#f7e6ff", fg="#660066", font=("Arial", 12))
        entry_nueva_cantidad.pack(pady=5)
        entry_nueva_cantidad.insert(0, cantidad[posicion])

        entry_nuevo_producto = tk.Entry(ventana_modificar, bg="#f7e6ff", fg="#660066", font=("Arial", 12))
        entry_nuevo_producto.pack(pady=5)
        entry_nuevo_producto.insert(0, productos[posicion])

        entry_nuevo_precio = tk.Entry(ventana_modificar, bg="#f7e6ff", fg="#660066", font=("Arial", 12))
        entry_nuevo_precio.pack(pady=5)
        entry_nuevo_precio.insert(0, precio[posicion])

        # Función para guardar cambios
        def guardar_cambios():
            nueva_cantidad = entry_nueva_cantidad.get()
            nuevo_producto = entry_nuevo_producto.get()
            nuevo_precio = entry_nuevo_precio.get()

            cantidad[posicion] = int(nueva_cantidad) if nueva_cantidad else cantidad[posicion]
            productos[posicion] = nuevo_producto if nuevo_producto else productos[posicion]
            precio[posicion] = int(nuevo_precio) if nuevo_precio else precio[posicion]

            messagebox.showinfo("Éxito", f"Producto '{buscador}' modificado con éxito.")
            ventana_modificar.destroy()

        # Botón para guardar cambios
        btn_guardar = tk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_cambios, bg="#ff66b2", fg="white", font=("Arial", 10, "bold"))
        btn_guardar.pack(pady=10)
        
    else:
        messagebox.showerror("Error", "Producto no encontrado.")
    limpiar_campos()

# Función para ver el inventario
def ver_productos():
    inventario = "Inventario Actual:\n"
    for i, prod in enumerate(productos):
        inventario += f"{i+1}. Producto: {prod} | Cantidad: {cantidad[i]} | Precio: ${precio[i]}\n"
    messagebox.showinfo("Inventario", inventario)

# Función para limpiar campos de entrada
def limpiar_campos():
    entry_cantidad.delete(0, tk.END)
    entry_producto.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# Crear y organizar los widgets
frame = tk.Frame(ventana, padx=10, pady=10, bg="#ffe6f2")
frame.pack(pady=20)

# Etiquetas y entradas con colores
tk.Label(frame, text="Cantidad:", bg="#ffe6f2", fg="#8c008c", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_cantidad = tk.Entry(frame, bg="#f7e6ff", fg="#660066", font=("Arial", 12))
entry_cantidad.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Producto:", bg="#ffe6f2", fg="#8c008c", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_producto = tk.Entry(frame, bg="#f7e6ff", fg="#660066", font=("Arial", 12))
entry_producto.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Precio:", bg="#ffe6f2", fg="#8c008c", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_precio = tk.Entry(frame, bg="#f7e6ff", fg="#660066", font=("Arial", 12))
entry_precio.grid(row=2, column=1, padx=5, pady=5)

# Botones con colores
btn_anadir = tk.Button(frame, text="Añadir Producto", command=anadir_producto, bg="#ff66b2", fg="white", font=("Arial", 10, "bold"))
btn_anadir.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

btn_buscar = tk.Button(frame, text="Buscar y Modificar", command=buscar_producto, bg="#cc33ff", fg="white", font=("Arial", 10, "bold"))
btn_buscar.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

btn_ver = tk.Button(frame, text="Ver Inventario", command=ver_productos, bg="#ff66b2", fg="white", font=("Arial", 10, "bold"))
btn_ver.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

# Iniciar la ventana principal
ventana.mainloop()
