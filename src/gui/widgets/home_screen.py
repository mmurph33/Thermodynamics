import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QLinearGradient, QTextCursor, QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QFormLayout, QTextBrowser
sys.path.append('/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/src')
from ProblemCode.Find_P_With_Fugacity import find_pressure
matplotlib.use('Agg')  # Set the backend to Agg



# ... [rest of your previous imports and code]
class VaporPressureWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vapor Pressure in Phase Equilibrium')
        self.setGeometry(250, 250, 800, 600)
        self.showMaximized()  # Maximizes the window
        
        self.layout = QVBoxLayout()

        # Input Fields
        self.input_layout = QFormLayout()
        self.temperature_input = QLineEdit(self)
        self.substance_input = QLineEdit(self)
        self.input_layout.addRow("Temperature (K):", self.temperature_input)
        self.input_layout.addRow("Substance:", self.substance_input)
        self.layout.addLayout(self.input_layout)

        self.calculate_btn = QPushButton("Calculate Vapor Pressure", self)
        self.calculate_btn.clicked.connect(self.calculate_vapor_pressure)
        self.layout.addWidget(self.calculate_btn)
        
        # Using QGridLayout to arrange the results in two columns
        self.results_layout = QVBoxLayout()
        self.layout.addLayout(self.results_layout)
        self.setLayout(self.layout)

    def _create_result_widget(self, P_in_MPa, result):
        """Utility function to create a result widget for a given result dictionary."""
        widget = QWidget(self)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Pressure: {P_in_MPa:.5f} MPa"))
        
        table = QTableWidget()
        table.setRowCount(1)
        table.setColumnCount(len(result) - 3)  # excluding 'iteration', 'is_correct', and 'P'
        table.setHorizontalHeaderLabels([key for key in result.keys() if key not in ['iteration', 'is_correct', 'P']])
        table.verticalHeader().setVisible(False)
        for col_idx, (key, value) in enumerate([(k, v) for k, v in result.items() if k not in ['iteration', 'is_correct', 'P']]):
            table.setItem(0, col_idx, QTableWidgetItem(f"{value:.4f}"))
        table.resizeColumnsToContents()

        layout.addWidget(table)

        if not result['is_correct']:
            latex_str = r"\phi^V \neq \phi^L, \text{so we will try a new pressure.} \; P_{\text{new}} = P_{\text{old}} \times \frac{\phi^L}{\phi^V}"
            pixmap = self.latex_to_QPixmap(latex_str)
            label = QLabel(self)
            label.setPixmap(pixmap)
            layout.addWidget(label)

        widget.setLayout(layout)

        return widget



    def latex_to_QPixmap(self, latex_str, fs=12):
        try:
            # Use LaTeX's default 'Computer Modern' font
            plt.rcParams['mathtext.fontset'] = 'cm'
            plt.rcParams['mathtext.rm'] = 'serif'

            # Create a figure and axis for rendering
            fig, ax = plt.subplots(figsize=(4, .40), dpi=120)
            
            # Set dark background and white text
            fig.patch.set_facecolor('#2f2f2f')  # Dark grey color for background
            ax.set_facecolor('#2f2f2f')
            
            # Render LaTeX in white
            ax.text(0.5, 0.5, f"${latex_str}$", size=fs, ha="center", va="center", color='white')
            ax.axis("off")

            # Adjust the margins to make sure the text fits
            plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

            # Draw the figure and retrieve the RGBA buffer
            fig.canvas.draw()
            buf = fig.canvas.buffer_rgba()
            
            # Convert to a QImage and then QPixmap
            qimage = QImage(buf, buf.shape[1], buf.shape[0], QImage.Format_RGBA8888)
            qpixmap = QPixmap.fromImage(qimage)
            
            plt.close(fig)
            return qpixmap
        except Exception as e:
            print(f"Error rendering LaTeX: {e}")
            return QPixmap()
    
    def calculate_vapor_pressure(self):
        T = float(self.temperature_input.text())
        substance = self.substance_input.text()

        # Fetch the results from the find_pressure function
        results = find_pressure(T, substance)

        # Clear previous results
        for i in reversed(range(self.results_layout.count())): 
            self.results_layout.itemAt(i).widget().setParent(None)

        # Create a main layout to hold the two columns
        main_hlayout = QHBoxLayout()

        # Create left and right QVBoxLayouts for the two columns
        left_vlayout = QVBoxLayout()
        right_vlayout = QVBoxLayout()

        # Split the results approximately in half
        half_length = len(results) // 2 

        for idx in range(half_length):
            # First column
            result1 = results[idx]
            P_in_MPa1 = result1['P'] / 1e6
            left_vlayout.addWidget(self._create_result_widget(P_in_MPa1, result1))

            # Check if there's a corresponding result in the second column
            if idx + half_length < len(results):
                result2 = results[idx + half_length]
                P_in_MPa2 = result2['P'] / 1e6
                right_vlayout.addWidget(self._create_result_widget(P_in_MPa2, result2))

        # Add the left and right QVBoxLayouts to the main QHBoxLayout
        main_hlayout.addLayout(left_vlayout)
        main_hlayout.addLayout(right_vlayout)

        # Add the main QHBoxLayout to the main results layout
        self.results_layout.addLayout(main_hlayout)
        self.results_layout.addWidget(QLabel("Pressure is correct since phi^V = phi^L."))

# ... [rest of your code]



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
