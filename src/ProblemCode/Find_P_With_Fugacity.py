"""
Calculates the fugacity coefficient using the Peng-Robinson equation of state.

Args:
    Z (float): The compressibility factor.
    A_val (float): The A parameter of the Peng-Robinson equation.
    B_val (float): The B parameter of the Peng-Robinson equation.

Returns:
    float: The fugacity coefficient.

Examples:
    > phi(0.9, 0.5, 0.3)
    0.987654321
"""

"""
Calculates various thermodynamic values using the Peng-Robinson equation of state.

Args:
    T (float): The temperature in Kelvin.
    P (float): The pressure in Pascal.
    T_C (float): The critical temperature of the substance.
    P_C (float): The critical pressure of the substance.
    omega (float): The acentric factor of the substance.

Returns:
    tuple: A tuple containing the calculated values:
        - a_T (float): The temperature-dependent parameter a.
        - b_val (float): The parameter b.
        - A_val (float): The parameter A.
        - B_val (float): The parameter B.
        - Z_values (list): The roots of the compressibility factor equation.
        - Zv (float): The first root of the compressibility factor equation.
        - Zl (float): The third root of the compressibility factor equation.
        - phi_Zv_value (float): The fugacity coefficient at Zv.
        - phi_Zl_value (float): The fugacity coefficient at Zl.

Examples:
    > calculate_values(298.15, 1e6, 190.6, 4.89e6, 0.0115)
    (0.000123456, 0.000987654, 0.000654321, 0.000321654, [0.9, 1.2, 1.5], 0.9, 1.5, 0.987654321, 0.87654321)
"""

"""
Finds the pressure at which the fugacity coefficients of the vapor and liquid phases are equal.

Args:
    T (float): The temperature in Kelvin.
    substance_name (str): The name of the substance.
    initial_guess (float, optional): The initial guess for the pressure. Defaults to 0.07e6.
    tolerance (float, optional): The tolerance for the difference between the fugacity coefficients. Defaults to 1e-6.
    max_iterations (int, optional): The maximum number of iterations. Defaults to 1000.

Returns:
    list: A list of dictionaries containing the results of each iteration. Each dictionary contains the following keys:
        - iteration (int): The iteration number.
        - P (float): The pressure in MPa.
        - A (float): The parameter A.
        - B (float): The parameter B.
        - Zv (float): The first root of the compressibility factor equation.
        - Zl (float): The third root of the compressibility factor equation.
        - phi_Zv (float): The fugacity coefficient at Zv.
        - phi_Zl (float): The fugacity coefficient at Zl.
        - is_correct (bool): Indicates if the fugacity coefficients are within the tolerance.

Examples:
    > find_pressure(298.15, 'methane', initial_guess=0.07e6, tolerance=1e-6, max_iterations=1000)
    [{'iteration': 1, 'P': 0.07, 'A': 0.000654321, 'B': 0.000321654, 'Zv': 0.9, 'Zl': 1.5, 'phi_Zv': 0.987654321, 'phi_Zl': 0.87654321, 'is_correct': False},
     {'iteration': 2, 'P': 0.065, 'A': 0.000654321, 'B': 0.000321654, 'Zv': 0.9, 'Zl': 1.5, 'phi_Zv': 0.987654321, 'phi_Zl': 0.87654321, 'is_correct': False},
     ...
     {'iteration': 10, 'P': 0.055, 'A': 0.000654321, 'B': 0.000321654, 'Zv': 0.9, 'Zl': 1.5, 'phi_Zv': 0.987654321, 'phi_Zl': 0.87654321, 'is_correct': True}]
"""
import sys
import numpy as np
import math
from src.core import PengRobinsonEOS, DatabaseHandler
import math

def phi(Z, A_val, B_val):
    term1 = (Z - 1)
    term2 = -math.log(max(Z - B_val, 0))
    numerator = max(Z + (1 + math.sqrt(2)) * B_val, 0)
    denominator = max(Z + (1 - math.sqrt(2)) * B_val, 0)
    term3 = - (1 / (2 * math.sqrt(2))) * (A_val / B_val) * math.log(numerator / denominator)
    return math.exp(term1 + term2 + term3)

def calculate_values(T, P, T_C, P_C, omega):
    a_T = PengRobinsonEOS.a(T, T_C, P_C, omega)
    b_val = PengRobinsonEOS.b(T_C, P_C)
    A_val = PengRobinsonEOS.A(a_T, P, T)
    B_val = PengRobinsonEOS.B(b_val, P, T)
    Z_values = PengRobinsonEOS.roots_of_Z(A_val, B_val)
    Zv = Z_values[0]  # First root
    Zl = Z_values[2]  # Third root
    phi_Zv_value = phi(Zv, A_val, B_val)
    phi_Zl_value = phi(Zl, A_val, B_val)
    return a_T, b_val, A_val, B_val, Z_values, Zv, Zl, phi_Zv_value, phi_Zl_value

def find_pressure(T, substance_name, initial_guess=0.07e6, tolerance=1e-6, max_iterations=1000):
    T_C, P_C, omega = DatabaseHandler.get_substance_parameters(substance_name)

    if not T_C:
        print(f"Error: Substance '{substance_name}' not found in the database.")
        return None

    P = initial_guess

    all_results = []

    for iteration in range(max_iterations):
        a_T, b_val, A_val, B_val, Z_values, Zv, Zl, phi_Zv_value, phi_Zl_value = calculate_values(T, P, T_C, P_C, omega)

        results = {
            'iteration': iteration + 1,
            'P': P / 1e6,
            'A': A_val,
            'B': B_val,
            'Zv': Zv,
            'Zl': Zl,
            'phi_Zv': phi_Zv_value,
            'phi_Zl': phi_Zl_value,
            'is_correct': abs(phi_Zv_value - phi_Zl_value) < tolerance,
        }
        all_results.append(results)

        if results['is_correct']:
            break
        P = P * (phi_Zl_value / phi_Zv_value)

    return all_results