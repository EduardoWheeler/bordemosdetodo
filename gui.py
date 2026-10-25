import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QMessageBox, QHeaderView
)

# Importamos el repositorio y el modelo del dominio
from repositorios.parche_repository import ParcheRepository
from modelos.parche import Parche

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bordemos De Todo - Gestión de Stock de Parches")
        self.resize(800, 550)

        # Instancia de la capa de repositorios
        self.repo_parche = ParcheRepository()
        self.id_seleccionado = None  # Almacena el ID del parche seleccionado en la tabla

        # Configuración del widget contenedor principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout(self.central_widget)

        # 1. Tabla de Parches
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Stock", "Cat. ID"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.itemSelectionChanged.connect(self.cargar_seleccion_tabla)
        self.layout_principal.addWidget(self.tabla)

        # 2. Formulario de Carga y Edición
        self.layout_form = QHBoxLayout()
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre del Parche")
        self.layout_form.addWidget(self.input_nombre)

        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Precio")
        self.layout_form.addWidget(self.input_precio)

        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("Stock")
        self.layout_form.addWidget(self.input_stock)

        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText("ID Categoría")
        self.layout_form.addWidget(self.input_categoria)

        self.layout_principal.addLayout(self.layout_form)

        # 3. Botones de Acción CRUD
        self.layout_botones = QHBoxLayout()
        
        self.btn_cargar = QPushButton("Refrescar Tabla")
        self.btn_cargar.clicked.connect(self.cargar_datos)
        self.layout_botones.addWidget(self.btn_cargar)

        self.btn_guardar = QPushButton("Guardar Nuevo")
        self.btn_guardar.clicked.connect(self.guardar_parche)
        self.layout_botones.addWidget(self.btn_guardar)

        self.btn_actualizar = QPushButton("Modificar Seleccionado")
        self.btn_actualizar.clicked.connect(self.actualizar_parche)
        self.layout_botones.addWidget(self.btn_actualizar)

        self.btn_eliminar = QPushButton("Eliminar Seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_parche)
        self.layout_botones.addWidget(self.btn_eliminar)

        self.layout_principal.addLayout(self.layout_botones)

        # Cargar datos al iniciar
        self.cargar_datos()

    def limpiar_formulario(self):
        """Limpia los inputs y reinicia la selección."""
        self.input_nombre.clear()
        self.input_precio.clear()
        self.input_stock.clear()
        self.input_categoria.clear()
        self.id_seleccionado = None
        self.tabla.clearSelection()

    def cargar_datos(self):
        """Consulta la base de datos a través del repositorio y llena la tabla."""
        try:
            parches = self.repo_parche.listar()
            self.tabla.setRowCount(0)
            for row, p in enumerate(parches):
                self.tabla.insertRow(row)
                # Guardamos el objeto entero o el ID en el primer item usando UserRole si se desea, 
                # pero aquí extraemos visualmente las propiedades
                item_id = QTableWidgetItem(str(p.id))
                item_id.setData(32, p)  # Guardamos el objeto Parche completo en los datos del item
                
                self.tabla.setItem(row, 0, item_id)
                self.tabla.setItem(row, 1, QTableWidgetItem(p.nombre))
                self.tabla.setItem(row, 2, QTableWidgetItem(str(p.precio)))
                self.tabla.setItem(row, 3, QTableWidgetItem(str(p.stock)))
                self.tabla.setItem(row, 4, QTableWidgetItem(str(p.categoria_id)))
            
            self.limpiar_formulario()
        except Exception as e:
            QMessageBox.critical(self, "Error de Conexión", f"No se pudieron cargar los datos: {e}")

    def cargar_seleccion_tabla(self):
        """Rellena los inputs automáticamente al hacer clic en una fila de la tabla."""
        seleccion = self.tabla.selectedItems()
        if not seleccion:
            return
        
        row = seleccion[0].row()
        # Recuperamos el objeto Parche almacenado en la columna 0
        item_0 = self.tabla.item(row, 0)
        parche_obj = item_0.data(32)

        if parche_obj:
            self.id_seleccionado = parche_obj.id
            self.input_nombre.setText(parche_obj.nombre)
            self.input_precio.setText(str(parche_obj.precio))
            self.input_stock.setText(str(parche_obj.stock))
            self.input_categoria.setText(str(parche_obj.categoria_id))

    def guardar_parche(self):
        """Inserta un nuevo registro utilizando la capa de negocio y repositorios."""
        try:
            nombre = self.input_nombre.text().strip()
            precio = int(self.input_precio.text())
            stock = int(self.input_stock.text())
            categoria_id = int(self.input_categoria.text())

            nuevo_parche = Parche(
                nombre=nombre,
                precio=precio,
                stock=stock,
                categoria_id=categoria_id
            )

            nuevo_id = self.repo_parche.insertar(nuevo_parche)
            QMessageBox.information(self, "Éxito", f"Parche registrado correctamente con ID: {nuevo_id}")
            self.cargar_datos()
        except ValueError as ve:
            QMessageBox.warning(self, "Atención", f"Datos de entrada inválidos: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el parche: {e}")

    def actualizar_parche(self):
        """Actualiza el registro seleccionado en la tabla."""
        if not self.id_seleccionado:
            QMessageBox.warning(self, "Atención", "Selecciona un parche de la tabla para modificar.")
            return

        try:
            nombre = self.input_nombre.text().strip()
            precio = int(self.input_precio.text())
            stock = int(self.input_stock.text())
            categoria_id = int(self.input_categoria.text())

            parche_actualizado = Parche(
                id=self.id_seleccionado,
                nombre=nombre,
                precio=precio,
                stock=stock,
                categoria_id=categoria_id
            )

            exito = self.repo_parche.actualizar(parche_actualizado)
            if exito:
                QMessageBox.information(self, "Éxito", "Parche actualizado correctamente.")
                self.cargar_datos()
            else:
                QMessageBox.warning(self, "Aviso", "No se pudo actualizar el registro.")
        except ValueError as ve:
            QMessageBox.warning(self, "Atención", f"Datos inválidos: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar: {e}")

    def eliminar_parche(self):
        """Elimina lógicamente/físicamente el parche seleccionado de la base de datos."""
        if not self.id_seleccionado:
            QMessageBox.warning(self, "Atención", "Selecciona un parche de la tabla para eliminar.")
            return

        confirmacion = QMessageBox.question(
            self, "Confirmar Eliminación", 
            "¿Estás seguro de que deseas eliminar este parche?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                exito = self.repo_parche.eliminar(self.id_seleccionado)
                if exito:
                    QMessageBox.information(self, "Éxito", "Parche eliminado correctamente.")
                    self.cargar_datos()
                else:
                    QMessageBox.warning(self, "Aviso", "No se encontró el registro para eliminar.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el registro: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())