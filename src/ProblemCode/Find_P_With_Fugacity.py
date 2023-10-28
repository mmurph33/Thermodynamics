import sys
import numpy as np
import math
sys.path.append('/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/src')
from peng_rob.core import PengRobinsonEOS, DatabaseHandler

# phi function with checks for negative logarithm arguments
def phi(Z, A_val, B_val):
    term1 = (Z - 1)
    term2 = -math.log(Z - B_val) if Z > B_val else 0
    numerator = (Z + (1 + math.sqrt(2)) * B_val)
    denominator = (Z + (1 - math.sqrt(2)) * B_val)
    if numerator > 0 and denominator > 0:
        term3 = - (1 / (2 * math.sqrt(2))) * (A_val / B_val) * math.log(numerator / denominator)
    else:
        term3 = 0
    return math.exp(term1 + term2 + term3)

def find_pressure(T, substance_name, initial_guess=1.235e6, tolerance=1e-6, max_iterations=1000):
    T_C, P_C, omega = DatabaseHandler.get_substance_parameters(substance_name)
    
    if not T_C:
        print(f"Error: Substance '{substance_name}' not found in the database.")
        return None

    P = initial_guess
    iteration = 0
    
    while iteration < max_iterations:
        # Calculate a(T), b, A, and B for the given conditions
        a_T = PengRobinsonEOS.a(T, T_C, P_C, omega)
        b_val = PengRobinsonEOS.b(T_C, P_C)
        A_val = PengRobinsonEOS.A(a_T, P, T)
        B_val = PengRobinsonEOS.B(b_val, P, T)
        
        # Get Z values (Z^V and Z^L)
        Z_values = get_Z_values(A_val, B_val)
        Zv = Z_values[0]  # First root
        Zl = Z_values[2]  # Third root
        
        # Compute phi values for Z^L and Z^V
        phi_Zv_value = phi(Zv, A_val, B_val)
        phi_Zl_value = phi(Zl, A_val, B_val)
        
        # Check if phi^V is approximately equal to phi^L
        if abs(phi_Zv_value - phi_Zl_value) < tolerance:
            break
        
        # Update the pressure
        P = P * (phi_Zl_value / phi_Zv_value)
        iteration += 1

    # Display the variables in a readable format
    print("\nCalculated Variables:")
    print(f"a(T): {a_T:.6f} J^2/mol^2")
    print(f"b: {b_val:.6f} m^3/mol")
    print(f"A: {A_val:.6f}")
    print(f"B: {B_val:.6f}")
    print(f"Z^V: {Zv:.6f}")
    print(f"Z^L: {Zl:.6f}")
    print(f"phi^V: {phi_Zv_value:.6f}")
    print(f"phi^L: {phi_Zl_value:.6f}")
    print(f"Pressure (in MPa): {P/1e6:.6f}")
    return P

def get_Z_values(A, B):
    # Coefficients of the Peng-Robinson EoS polynomial
    coefficients = [1, 
                    -(1-B), 
                    A - 2*B - 3*B**2, 
                    -A*B + B**2 + B**3]
    
    # Get the roots of the polynomial
    Z_values = np.roots(coefficients)
    
    # Sort the Z values in descending order
    Z_values = sorted(Z_values, reverse=True)
    
    return Z_values
