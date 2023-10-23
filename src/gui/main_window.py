import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QFormLayout, QLineEdit, QLabel)
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, 
                                                NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
sys.path.append('/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/src')

from peng_rob.core import (get_substance_parameters, calculate_parameters, roots_of_Z)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Roots of Z using Peng-Robinson EOS')
        self.setGeometry(100, 100, 1000, 800)

        layout = QVBoxLayout()

        # Input fields
        form_layout = QFormLayout()
        self.substance_input = QLineEdit(self)
        self.temperature_input = QLineEdit(self)
        self.pressure_input = QLineEdit(self)
        form_layout.addRow('Substance:', self.substance_input)
        form_layout.addRow('Temperature (K):', self.temperature_input)
        form_layout.addRow('Pressure (Pa):', self.pressure_input)

        # Plot button
        self.plot_button = QPushButton('Calculate & Plot', self)
        self.plot_button.clicked.connect(self.plot_roots_of_Z)

        # Output field
        self.molar_volume_label = QLabel("Molar Volume: Not Calculated", self)

        # Matplotlib Figure and Canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add to layout
        layout.addLayout(form_layout)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.molar_volume_label)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def plot_roots_of_Z(self):
        substance = self.substance_input.text()
        T = float(self.temperature_input.text())
        P = float(self.pressure_input.text())

        T_C, P_C, omega = get_substance_parameters(substance)

        if T_C and P_C and omega:
            a_val, b_val, A_val, B_val = calculate_parameters(T, T_C, P_C, omega, P)
            Z_roots = roots_of_Z(A_val, B_val)
            
            # Plotting
            self.ax.clear()
            P_array = [P] * len(Z_roots)
            self.ax.plot(P_array, Z_roots, 'o')
            self.ax.set_xlabel('Pressure (Pa)')
            self.ax.set_ylabel('Z')
            self.ax.set_title('Roots of Compressibility Factor (Z) vs Pressure')
            self.canvas.draw()

            # Assuming you want to use the largest Z root for molar volume
            Z = max(Z_roots)
            R = 8.314  # Universal gas constant in J/(mol·K)
            V = Z * R * T / P
            self.molar_volume_label.setText(f"Molar Volume: {V:.5f} m^3/mol")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
