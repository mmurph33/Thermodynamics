import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QFormLayout, QLineEdit, QLabel)
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, 
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
sys.path.append('/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/src')

from src.ProblemCode.core import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Thermodynamics Assistant')
        self.setGeometry(100, 100, 1000, 800)

        layout = QVBoxLayout()

        # Problem selection buttons
        self.molar_volume_button = QPushButton('Solve for Molar Volume', self)
        self.molar_volume_button.clicked.connect(self.solve_molar_volume)

        self.enthalpy_button = QPushButton('Find Change in Enthalpy Using PREOS', self)
        self.enthalpy_button.clicked.connect(self.solve_enthalpy)

        self.entropy_button = QPushButton('Find Change in Entropy Using PREOS', self)
        self.entropy_button.clicked.connect(self.solve_entropy)

        self.vapor_pressure_button = QPushButton('Find Vapor Pressure in Phase Equilibrium', self)
        self.vapor_pressure_button.clicked.connect(self.solve_vapor_pressure)

        self.thermo_properties_button = QPushButton('Find Thermodynamics Properties of a Substance', self)
        self.thermo_properties_button.clicked.connect(self.solve_thermo_properties)

        # Add buttons to layout
        layout.addWidget(self.molar_volume_button)
        layout.addWidget(self.enthalpy_button)
        layout.addWidget(self.entropy_button)
        layout.addWidget(self.vapor_pressure_button)
        layout.addWidget(self.thermo_properties_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Placeholder methods for each problem-solving option
    def solve_molar_volume(self):
        pass

    def solve_enthalpy(self):
        pass

    def solve_entropy(self):
        pass

    def solve_vapor_pressure(self):
        pass

    def solve_thermo_properties(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
