# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 23:25:00 2024

@author: celes
"""






import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QFileDialog, QMessageBox, QComboBox, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

class InventarioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario de PHYTODELICIA°")
        self.setGeometry(500, 500, 800, 600)
        self.setStyleSheet("background-color: #F5E6E8;")

        # Variables
        self.ruta_excel = None
        self.df = None
        self.sheet_name = None

        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Logo
        logo = QLabel(self)
        pixmap = QPixmap("C:/Users/celes/pruebas_inventario/logo.jpg")
        logo.setPixmap(pixmap.scaled(500, 150, Qt.AspectRatioMode.KeepAspectRatio))
        main_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Título
        titulo = QLabel("Gestión de Inventario")
        titulo.setStyleSheet("font-size: 20px; color: #8E44AD; font-weight: bold;")
        main_layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botones principales
        botones_layout = QHBoxLayout()

        self.boton_ver_inventario = QPushButton("Ver Inventario")
        self.boton_ver_inventario.clicked.connect(self.ver_inventario)
        botones_layout.addWidget(self.boton_ver_inventario)

        self.boton_añadir_modificar = QPushButton("Añadir o Modificar Artículo")
        self.boton_añadir_modificar.clicked.connect(self.abrir_formulario_agregar)
        botones_layout.addWidget(self.boton_añadir_modificar)

        self.boton_quitar_producto = QPushButton("Quitar Producto")
        self.boton_quitar_producto.clicked.connect(self.abrir_formulario_quitar)
        botones_layout.addWidget(self.boton_quitar_producto)

        # Botones de Salir y Guardar
        botones_guardar_salir = QHBoxLayout()
        self.boton_guardar_y_salir = QPushButton("Guardar y Salir")
        self.boton_guardar_y_salir.clicked.connect(self.guardar_y_salir)
        botones_guardar_salir.addWidget(self.boton_guardar_y_salir)

        self.boton_salir = QPushButton("Salir sin Guardar")
        self.boton_salir.clicked.connect(self.close)
        botones_guardar_salir.addWidget(self.boton_salir)

        main_layout.addLayout(botones_layout)
        main_layout.addLayout(botones_guardar_salir)

        # Estilo para los botones
        button_style = """
            QPushButton {
                background-color: #D98880;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
        """
        self.boton_ver_inventario.setStyleSheet(button_style)
        self.boton_añadir_modificar.setStyleSheet(button_style)
        self.boton_quitar_producto.setStyleSheet(button_style)
        self.boton_guardar_y_salir.setStyleSheet(button_style)
        self.boton_salir.setStyleSheet(button_style)

    def seleccionar_archivo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx)")
        if file_path:
            self.ruta_excel = file_path
            return True
        return False

    def seleccionar_hoja(self):
        if not self.ruta_excel:
            return None
    
        try:
            # Cargar el archivo Excel y obtener los nombres de las hojas
            libro = pd.ExcelFile(self.ruta_excel)
            hojas = libro.sheet_names
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar el archivo Excel: {e}")
            return None
    
        # Crear diálogo para seleccionar la hoja
        dialog = QDialog(self)
        dialog.setWindowTitle("Seleccionar Hoja")
    
        layout = QVBoxLayout()
        combo_sheets = QComboBox(dialog)
        combo_sheets.addItems(hojas)  # Agregar todas las hojas al combo
        layout.addWidget(combo_sheets)
    
        # Botones de aceptar y cancelar
        botones_layout = QHBoxLayout()
        boton_aceptar = QPushButton("Aceptar", dialog)
        boton_aceptar.clicked.connect(dialog.accept)
        boton_cancelar = QPushButton("Cancelar", dialog)
        boton_cancelar.clicked.connect(dialog.reject)
    
        botones_layout.addWidget(boton_aceptar)
        botones_layout.addWidget(boton_cancelar)
        layout.addLayout(botones_layout)
    
        dialog.setLayout(layout)
        if dialog.exec():
            self.sheet_name = combo_sheets.currentText()
            return self.sheet_name
        return None
    
    def ver_inventario(self):
        if not self.seleccionar_archivo():
            QMessageBox.warning(self, "Advertencia", "Selecciona un archivo Excel primero.")
            return

        sheet = self.seleccionar_hoja()
        if not sheet:
            return

        self.df = pd.read_excel(self.ruta_excel, sheet_name=sheet)

        # Crea una ventana para mostrar el inventario
        self.ventana_ver = QWidget()
        self.ventana_ver.setWindowTitle("Ver Inventario")
        self.ventana_ver.setGeometry(150, 150, 800, 400)
        layout = QVBoxLayout()
        
        # Tabla de productos
        self.table = QTableWidget()
        self.table.setRowCount(self.df.shape[0])
        self.table.setColumnCount(self.df.shape[1])
        self.table.setHorizontalHeaderLabels(self.df.columns)
        
        for i, row in self.df.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        self.ventana_ver.setLayout(layout)
        self.ventana_ver.show()

    def abrir_formulario_agregar(self):
        if not self.seleccionar_archivo():
            QMessageBox.warning(self, "Advertencia", "Selecciona un archivo Excel primero.")
            return

        sheet = self.seleccionar_hoja()
        if not sheet:
            return

        self.df = pd.read_excel(self.ruta_excel, sheet_name=sheet)

        # Ventana para añadir o modificar artículo
        self.ventana_agregar = QWidget()
        self.ventana_agregar.setWindowTitle("Añadir o Modificar Artículo")
        self.ventana_agregar.setGeometry(200, 200, 400, 400)
        layout = QVBoxLayout()

        # Campos de entrada
        self.campos = {}
        for columna in ["Contenedor", "Etiqueta", "Nombre", "Subtitulo", "Marca", "F. vencimiento", "Detalle", "Unidades"]:
            label = QLabel(f"{columna}:")
            campo = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(campo)
            self.campos[columna] = campo

        boton_guardar = QPushButton("Guardar Producto")
        boton_guardar.clicked.connect(self.guardar_producto)
        layout.addWidget(boton_guardar)
        
        self.ventana_agregar.setLayout(layout)
        self.ventana_agregar.show()

    def guardar_producto(self):
        datos = {columna: campo.text() for columna, campo in self.campos.items()}
        
        indice = self.df[self.df['Nombre'] == datos["Nombre"]].index
        if not indice.empty:
            self.df.loc[indice, :] = datos
        else:
            self.df = pd.concat([self.df, pd.DataFrame([datos])], ignore_index=True)

        QMessageBox.information(self, "Guardado", "Producto añadido o modificado correctamente.")
        self.ventana_agregar.close()

    def abrir_formulario_quitar(self):
        self.ventana_quitar = QWidget()
        self.ventana_quitar.setWindowTitle("Quitar Producto")
        self.ventana_quitar.setGeometry(200, 200, 400, 200)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nombre del Producto a Quitar:"))
        self.campo_nombre_quitar = QLineEdit()
        layout.addWidget(self.campo_nombre_quitar)

        layout.addWidget(QLabel("Cantidad a Quitar:"))
        self.campo_cantidad_quitar = QLineEdit()
        layout.addWidget(self.campo_cantidad_quitar)

        boton_quitar = QPushButton("Quitar Producto")
        boton_quitar.clicked.connect(self.quitar_producto)
        layout.addWidget(boton_quitar)
        
        self.ventana_quitar.setLayout(layout)
        self.ventana_quitar.show()

    def quitar_producto(self):
        nombre_producto = self.campo_nombre_quitar.text()
        cantidad_quitar = int(self.campo_cantidad_quitar.text())

        indice = self.df[self.df['Nombre'] == nombre_producto].index
        if not indice.empty:
            self.df.loc[indice, 'Unidades'] = max(0, self.df.loc[indice, 'Unidades'] - cantidad_quitar)
            QMessageBox.information(self, "Quitar", "Producto quitado correctamente.")
            self.ventana_quitar.close()
        else:
            QMessageBox.warning(self, "Error", "Producto no encontrado.")

    def guardar_y_salir(self):
        if self.ruta_excel and self.sheet_name:
            with pd.ExcelWriter(self.ruta_excel, mode="a", if_sheet_exists="replace") as writer:
                self.df.to_excel(writer, sheet_name=self.sheet_name, index=False)
        self.close()

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("C:/Users/celes/pruebas_inventario/logo.jpg"))
ventana = InventarioApp()
ventana.show()
sys.exit(app.exec())
