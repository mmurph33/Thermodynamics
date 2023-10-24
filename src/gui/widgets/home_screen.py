import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt

class MolarVolumeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Molar Volume Solver')
        self.setGeometry(250, 250, 600, 400)
        layout = QVBoxLayout()
        label = QLabel("Solve for Molar Volume", self)
        layout.addWidget(label)
        self.setLayout(layout)


class EnthalpyPREOSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enthalpy Using PREOS Solver')
        self.setGeometry(250, 250, 600, 400)
        layout = QVBoxLayout()
        label = QLabel("Find Change in Enthalpy Using PREOS", self)
        layout.addWidget(label)
        self.setLayout(layout)

class EntropyPREOSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Entropy Using PREOS Solver')
        self.setGeometry(250, 250, 600, 400)
        layout = QVBoxLayout()
        label = QLabel("Find Change in Entropy Using PREOS", self)
        layout.addWidget(label)
        self.setLayout(layout)

class VaporPressureWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vapor Pressure in Phase Equilibrium')
        self.setGeometry(250, 250, 600, 400)
        layout = QVBoxLayout()
        label = QLabel("Find Vapor Pressure in Phase Equilibrium", self)
        layout.addWidget(label)
        self.setLayout(layout)

class ThermoPropertiesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Thermodynamic Properties of Real Substances')
        self.setGeometry(250, 250, 600, 400)
        layout = QVBoxLayout()
        label = QLabel("Find Thermodynamic Properties of Real Substances", self)
        layout.addWidget(label)
        self.setLayout(layout)


class ThermoAssistantHome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        # Window Setup
        self.setWindowTitle("Thermodynamics Assistant")
        self.setGeometry(100, 100, 800, 600)

        # Custom Styling
        self.palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, QColor(50, 50, 50))
        self.palette.setBrush(QPalette.Window, gradient)
        self.setPalette(self.palette)
        
        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Title
        title = QLabel("Thermodynamics Assistant")
        title_font = QFont("Fira Code", 24, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: red;")
        layout.addWidget(title)

        # Buttons
        self.setup_buttons(layout)

        central_widget.setLayout(layout)

    def setup_buttons(self, layout):
        # Molar Volume Button
        self.molar_volume_btn = QPushButton('Solve for Molar Volume', self)
        self.molar_volume_btn.setFont(QFont("Fira Code", 14))
        self.molar_volume_btn.setStyleSheet("background-color: red; color: black;")
        self.molar_volume_btn.clicked.connect(self.open_molar_volume_window)
        layout.addWidget(self.molar_volume_btn)
        
        # Enthalpy Button
        self.enthalpy_btn = QPushButton('Find Change in Enthalpy Using PREOS', self)
        self.enthalpy_btn.setFont(QFont("Fira Code", 14))
        self.enthalpy_btn.setStyleSheet("background-color: red; color: black;")
        self.enthalpy_btn.clicked.connect(self.open_enthalpy_window)
        layout.addWidget(self.enthalpy_btn)
        
        # Entropy Button
        self.entropy_btn = QPushButton('Find Change in Entropy Using PREOS', self)
        self.entropy_btn.setFont(QFont("Fira Code", 14))
        self.entropy_btn.setStyleSheet("background-color: red; color: black;")
        self.entropy_btn.clicked.connect(self.open_entropy_window)
        layout.addWidget(self.entropy_btn)
        
        # Vapor Pressure Button
        self.vapor_pressure_btn = QPushButton('Find Vapor Pressure in Phase Equilibrium', self)
        self.vapor_pressure_btn.setFont(QFont("Fira Code", 14))
        self.vapor_pressure_btn.setStyleSheet("background-color: red; color: black;")
        self.vapor_pressure_btn.clicked.connect(self.open_vapor_pressure_window)
        layout.addWidget(self.vapor_pressure_btn)

        # Thermo Properties Button
        self.thermo_properties_btn = QPushButton('Find Thermodynamics Properties of a Substance', self)
        self.thermo_properties_btn.setFont(QFont("Fira Code", 14))
        self.thermo_properties_btn.setStyleSheet("background-color: red; color: black;")
        self.thermo_properties_btn.clicked.connect(self.open_thermo_properties_window)
        layout.addWidget(self.thermo_properties_btn)

    def open_molar_volume_window(self):
        self.molar_volume_window = MolarVolumeWindow()
        self.molar_volume_window.show()

    def open_enthalpy_window(self):
        self.enthalpy_window = EnthalpyPREOSWindow()
        self.enthalpy_window.show()

    def open_entropy_window(self):
        self.entropy_window = EntropyPREOSWindow()
        self.entropy_window.show()

    def open_vapor_pressure_window(self):
        self.vapor_pressure_window = VaporPressureWindow()
        self.vapor_pressure_window.show()

    def open_thermo_properties_window(self):
        self.thermo_properties_window = ThermoPropertiesWindow()
        self.thermo_properties_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThermoAssistantHome()
    window.show()
    sys.exit(app.exec_())
