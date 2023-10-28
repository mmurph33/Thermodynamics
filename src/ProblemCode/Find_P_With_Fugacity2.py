import sys
import numpy as np
import math
sys.path.append('/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/src')
from peng_rob.core import PengRobinsonEOS, DatabaseHandler

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
    
    all_results = []
    
    while iteration < max_iterations:
        iteration_results = {}
        iteration_results['P'] = P
        iteration_results['iteration'] = iteration + 1

        # Calculate a(T), b, A, and B for the given conditions
        a_T = PengRobinsonEOS.a(T, T_C, P_C, omega)
        b_val = PengRobinsonEOS.b(T_C, P_C)
        A_val = PengRobinsonEOS.A(a_T, P, T)
        B_val = PengRobinsonEOS.B(b_val, P, T)

        iteration_results['A'] = A_val
        iteration_results['B'] = B_val
        
        # Get Z values (Z^V and Z^L) using the PengRobinsonEOS methods
        Z_values = PengRobinsonEOS.roots_of_Z(A_val, B_val)
        Zv = Z_values[0]  # First root
        Zl = Z_values[2]  # Third root

        iteration_results['Zv'] = Zv
        iteration_results['Zl'] = Zl
        
        # Compute phi values for Z^L and Z^V
        phi_Zv_value = phi(Zv, A_val, B_val)
        phi_Zl_value = phi(Zl, A_val, B_val)

        iteration_results['phi_Zv'] = phi_Zv_value
        iteration_results['phi_Zl'] = phi_Zl_value
        
        all_results.append(iteration_results)

        # Check if phi^V is approximately equal to phi^L
        if abs(phi_Zv_value - phi_Zl_value) < tolerance:
            iteration_results['is_correct'] = True
            break
        else:
            iteration_results['is_correct'] = False
            # Update the pressure
            P = P * (phi_Zl_value / phi_Zv_value)
            iteration += 1
    
    return all_results
