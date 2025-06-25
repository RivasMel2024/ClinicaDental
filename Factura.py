from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import List

class Factura:
    def __init__(self, id_factura: str, paciente: Paciente, 
                 tratamientos: List[Tratamiento], fecha_emision: datetime, 
                 estado_pago: str):
        self.id_factura = id_factura
        self.paciente = paciente
        self.tratamientos = tratamientos
        self.fecha_emision = fecha_emision
        self.monto_total = 0.0
        self.estado_pago = estado_pago
        self.calcular_monto_total()

    def calcular_monto_total(self):
        self.monto_total = sum(tratamiento.costo for tratamiento in self.tratamientos)

    def __str__(self):
        return (f"Factura{{idFactura='{self.id_factura}', "
                f"paciente={self.paciente}, "
                f"montoTotal={self.monto_total}, "
                f"estadoPago='{self.estado_pago}'}}")

class FacturaWindow(QMainWindow):
    def __init__(self, pacientes: List[Paciente]):
        super().__init__()
        self.setWindowTitle("Gestión de Facturas - Clínica Dental")
        self.setGeometry(100, 100, 800, 600)

        # Color scheme 
        self.colors = {
            'primary': '#130760',      
            'secondary': '#756f9f',   
            'accent': '#10b8b9',       
            'background': '#2b2b2b',   
            'surface': '#3c3c3c',      
            'text_light': '#ffffff',   
            'text_dark': '#e0e0e0'     
        }

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors['background']};
                font-family: 'Segoe UI';
                font-size: 14px;
                color: {self.colors['text_light']};
            }}
            
            QLabel {{
                color: {self.colors['text_light']};
                font-family: 'Segoe UI';
                font-size: 14px;
            }}
            
            QGroupBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['text_light']};
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                margin: 10px 0px;
                padding-top: 15px;
                background-color: {self.colors['surface']};
            }}
            
            QLineEdit, QDoubleSpinBox {{
                font-family: 'Segoe UI';
                font-size: 14px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 6px;
                padding: 10px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_light']};
                selection-background-color: {self.colors['accent']};
            }}
            
            QPushButton {{
                font-family: 'Segoe UI';
                font-size: 14px;
                font-weight: bold;
                color: {self.colors['text_light']};
                background-color: {self.colors['secondary']};
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 4px;
            }}
            
            QPushButton:hover {{
                background-color: {self.colors['accent']};
            }}
            
            QTextEdit {{
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 2px solid {self.colors['secondary']};
                border-radius: 8px;
                background-color: {self.colors['surface']};
                color: {self.colors['text_dark']};
                padding: 15px;
            }}
        """)

        self.facturas: List[Factura] = []  # lista de facturas
        self.pacientes = pacientes  # lista de pacientes existentes
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # scroll 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        title = QLabel("🧾 Sistema de Gestión de Facturas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_light']};
                background-color: {self.colors['surface']};
                border: 3px solid {self.colors['accent']};
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
            }}
        """)
        main_layout.addWidget(title)
        
        # info de la factura
        info_group = QGroupBox("Información de la Factura")
        info_layout = QFormLayout()
        
        self.id_factura_edit = QLineEdit()
        self.paciente_edit = QLineEdit()  # psible mejora: usar un QcomboBox para seleccionar los pacientes
        self.fecha_edit = QLineEdit()
        self.estado_pago_edit = QLineEdit()
        
        info_layout.addRow("ID de Factura:", self.id_factura_edit)
        info_layout.addRow("Paciente:", self.paciente_edit)
        info_layout.addRow("Fecha (DD/MM/AAAA):", self.fecha_edit)
        info_layout.addRow("Estado de Pago:", self.estado_pago_edit)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.crear_btn = QPushButton("➕ Crear Factura")
        self.crear_btn.clicked.connect(self.crear_factura)
        
        self.mostrar_btn = QPushButton("📋 Mostrar Facturas")
        self.mostrar_btn.clicked.connect(self.mostrar_facturas)
        
        buttons_layout.addWidget(self.crear_btn)
        buttons_layout.addWidget(self.mostrar_btn)
        
        main_layout.addLayout(buttons_layout)
        
        
        resultado_label = QLabel("📊 Resultados:")
        resultado_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        resultado_label.setStyleSheet(f"color: {self.colors['accent']};")
        main_layout.addWidget(resultado_label)
        
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)
        self.resultado_text.setFont(QFont("Consolas", 13))
        self.resultado_text.setPlaceholderText("Aquí aparecerán los resultados de las operaciones...")
        
        main_layout.addWidget(self.resultado_text)

    def crear_factura(self):
        """Crea una nueva factura con los datos ingresados"""
        id_factura = self.id_factura_edit.text().strip()
        paciente_nombre = self.paciente_edit.text().strip()
        fecha_emision = self.fecha_edit.text().strip()
        estado_pago = self.estado_pago_edit.text().strip()

        if not all([id_factura, paciente_nombre, fecha_emision, estado_pago]):
            QMessageBox.warning(self, "❌ Error", "Todos los campos son obligatorios")
            return

        # buscar el paciente existente desde el archivo de paciente
        paciente_existente = None
        for paciente in self.pacientes:
            if paciente.nombre == paciente_nombre:
                paciente_existente = paciente
                break

        if paciente_existente is None:
            QMessageBox.warning(self, "❌ Error", "Paciente no encontrado")
            return

        nueva_factura = Factura(id_factura, paciente_existente, [], datetime.now(), estado_pago)
        self.facturas.append(nueva_factura)

        QMessageBox.information(self, "✅ Éxito", f"Factura {id_factura} creada exitosamente.")
        self.resultado_text.append(str(nueva_factura))

    def mostrar_facturas(self):
        """Muestra todas las facturas registradas"""
        self.resultado_text.clear()
        if not self.facturas:
            QMessageBox.information(self, "ℹ️ Información", "No hay facturas registradas")
            return
        
        for factura in self.facturas:
            self.resultado_text.append(str(factura))

def main():
    app = QApplication([])
    
    # este es un ejemplo de como podemos cargra los pacientes pero podemos buscar otra opcion no tan manual 
    pacientes = [
        Paciente(1, "Laura", "Pérez", 27, "Femenino", "7012-3456", "laura.perez@example.com", "Santa Tecla"),
        Paciente(2, "Juan", "Gómez", 30, "Masculino", "6012-3456", "juan.gomez@example.com", "San Salvador")
    ]
    
    window = FacturaWindow(pacientes)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
