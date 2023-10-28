import matplotlib.pyplot as plt
import matplotlib.table as tbl
from Find_P_With_Fugacity import calculate_values, DatabaseHandler, PengRobinsonEOS

def plot_isotherm_and_table(T, substance_name):
    # Fetch substance parameters from the database
    T_C, P_C, omega = DatabaseHandler.get_substance_parameters(substance_name)
    
    # Define pressure range for the graph
    pressures = np.linspace(0, 2.5e6, 1000)  # Pressures from 0 to 2.5 MPa
    
    # Calculate Z values for the pressure range
    Zv_vals = []
    Zl_vals = []
    A_vals = []
    B_vals = []
    for P in pressures:
        _, _, A_val, B_val, _, Zv, Zl, _, _ = calculate_values(T, P, T_C, P_C, omega)
        Zv_vals.append(Zv)
        Zl_vals.append(Zl)
        A_vals.append(A_val)
        B_vals.append(B_val)
    
    # Graphing
    plt.figure(figsize=(10, 7))
    
    # Plot Z values
    plt.plot(pressures/1e6, Zv_vals, label=f"$Z^V$ for {substance_name}", color="blue")
    plt.plot(pressures/1e6, Zl_vals, label=f"$Z^L$ for {substance_name}", color="red")

    # Annotate the graph with the Z^V and Z^L values
    P_sample = 1e6  # Example pressure for annotation
    _, _, A_val, B_val, _, Zv, Zl, phi_Zv, phi_Zl = calculate_values(T, P_sample, T_C, P_C, omega)
    
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
    table_vals = [[f"{A_val:.5f}", f"{B_val:.5f}", f"{Zl:.5f}", f"{Zv:.5f}", f"{phi_Zl:.5f}", f"{phi_Zv:.
