import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QMessageBox, QHeaderView
)

# Importamos las capas sin modificar nada de su código original
from repositorios.parche_repository import ParcheRepository
from modelos.parche import Parche

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bordemos De Todo - Gestión de Parches")
        self.resize(750, 500)

        # Instancia de la capa de repositorios
        self.repo_parche = ParcheRepository()

        # Configuración del widget contenedor principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout(self.central_widget)

        # 1. Tabla de Parches
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "Stock", "Cat. ID"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout_principal.addWidget(self.tabla)

        # 2. Formulario simple para agregar
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

        # 3. Botones de Acción
        self.layout_botones = QHBoxLayout()

        self.btn_cargar = QPushButton("Cargar / Refrescar Tabla")
        self.btn_cargar.clicked.connect(self.cargar_datos)
        self.layout_botones.addWidget(self.btn_cargar)

        self.btn_guardar = QPushButton("Guardar Parche")
        self.btn_guardar.clicked.connect(self.guardar_parche)
        self.layout_botones.addWidget(self.btn_guardar)

        self.layout_principal.addLayout(self.layout_botones)

        # Cargar datos al iniciar
        self.cargar_datos()

    def cargar_datos(self):
        """Consume el método listar() del repositorio y actualiza la tabla."""
        try:
            parches = self.repo_parche.listar()
            self.tabla.setRowCount(0)

            for row, p in enumerate(parches):
                self.tabla.insertRow(row)
                self.tabla.setItem(row, 0, QTableWidgetItem(str(p.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(p.nombre))
                self.tabla.setItem(row, 2, QTableWidgetItem(f"${p.precio}"))
                self.tabla.setItem(row, 3, QTableWidgetItem(str(p.stock)))
                self.tabla.setItem(row, 4, QTableWidgetItem(str(p.categoria_id)))
        except Exception as e:
            QMessageBox.critical(self, "Error de Conexión", f"No se pudieron cargar los datos: {e}")

    def guardar_parche(self):
        """Crea el modelo Parche y utiliza el repositorio para darlo de alta."""
        try:
            nombre = self.input_nombre.text().strip()
            precio = int(self.input_precio.text())
            stock = int(self.input_stock.text())
            categoria_id = int(self.input_categoria.text())

            # Instanciamos el modelo del dominio
            nuevo_parche = Parche(
                nombre=nombre,
                precio=precio,
                stock=stock,
                categoria_id=categoria_id
            )

            # Insertamos en la base de datos a través del repositorio
            nuevo_id = self.repo_parche.insertar(nuevo_parche)
            QMessageBox.information(self, "Éxito", f"Parche registrado con ID: {nuevo_id}")

            # Limpiar campos y refrescar
            self.input_nombre.clear()
            self.input_precio.clear()
            self.input_stock.clear()
            self.input_categoria.clear()
            self.cargar_datos()

        except ValueError as ve:
            QMessageBox.warning(self, "Atención", f"Datos de entrada inválidos: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el parche: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())