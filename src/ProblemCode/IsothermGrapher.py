import matplotlib.pyplot as plt
import matplotlib.table as tbl
import numpy as np
from Find_P_With_Fugacity import calculate_values, DatabaseHandler, PengRobinsonEOS

def find_roots(v_range, T, T_C, P_C, omega, P_target):
    """Find roots of the equation P_PR - P_target = 0 using the Newton-Raphson method."""
    roots = []
    for v_initial in v_range:
        try:
            root = newton(lambda v: P_PR(v, T, T_C, P_C, omega) - P_target, v_initial)
            # Check if the root is unique
            if not any(np.isclose(root, r, atol=1e-6) for r in roots):
                roots.append(root)
        except RuntimeError:
            pass
    return roots

def plot_isotherm_and_table(T, substance_name, P_guess):
    # Fetch substance parameters from the database
    T_C, P_C, omega = DatabaseHandler.get_substance_parameters(substance_name)

    # Define pressure range for the graph
    v_values = np.linspace(1e-4, 0.1, 1000)  # Range of molar volumes
    P_values = PengRobinsonEOS.P_PR(v_values, T, T_C, P_C, omega)

    # Define the intersection_volumes and P_given variables
    intersection_volumes = []

    # Plot the isotherm curve
    plt.figure(figsize=(10, 7))
    plt.plot(v_values, P_values/1e5, label=f'Isotherm at T = {T} K', color='blue')  # Pressure in bars
    plt.axhline(P_given/1e5, color='green', linestyle='--', label=f'Given Pressure = {P_given/1e5} bar')  # Given pressure

    # Mark the intersection points
    for v in intersection_volumes:
        plt.plot(v, P_given/1e5, 'ro')

    # Define the calculate_values function
    def calculate_values(T, P_sample, T_C, P_C, omega):
        pass

# Example pressure for annotation

    plt.annotate(f"$Z^V$ = {Zv:.5f}", (P_sample/1e6, Zv), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
    plt.annotate(f"$Z^L$ = {Zl:.5f}", (P_sample/1e6, Zl), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8)

    # Formatting graph
    plt.title(f'Isotherm for {substance_name} at {T} K')
    plt.xlabel('Pressure (MPa)')
    plt.ylabel('Compressibility Factor, Z')
    plt.legend()
    plt.grid(True)

    # Creating the table below the graph
    col_labels = [r"$A$", r"$B$", r"$Z^l$", r"$Z^v$", r"$\phi^l$", r"$\phi^v$"]
    table_vals = [[f"{A_val:.5f}", f"{B_val:.5f}", f"{Zl:.5f}", f"{Zv:.5f}", f"{phi_Zl:.5f}", f"{phi_Zv:.5f}"]]

plot_isotherm_and_table(300, 'isopentane', 0.075e6)
