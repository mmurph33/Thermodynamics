import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.peng_rob.core import get_substance_parameters, calculate_parameters, roots_of_Z, enthalpy_departure, entropy_departure, da_dT
from scipy import constants

R = constants.R  # Universal gas constant in J/(mol·K)

if __name__ == "__main__":
    substance = input("Enter the name of the substance: ")

    # Getting temperature with unit handling
    T = float(input("Enter the temperature: "))
    T_units = input("Enter the units (default is Kelvin, options: 'Celsius', 'Fahrenheit'): ").lower()
    if T_units == 'celsius':
        T += 273.15  # Convert Celsius to Kelvin
    elif T_units == 'fahrenheit':
        T = (T - 32) * 5/9 + 273.15  # Convert Fahrenheit to Kelvin
    elif T_units != '':
        print("Unknown temperature unit. Assuming Kelvin.")
    
    # Getting pressure with unit handling
    P = float(input("Enter the pressure: "))
    P_units = input("Enter the units (default is Pa, options: 'atm', 'bar', 'psi'): ").lower()
    if P_units == 'atm':
        P *= constants.atm  # Convert atm to Pa
    elif P_units == 'bar':
        P *= 1e5  # Convert bar to Pa
    elif P_units == 'psi':
        P *= 6894.76  # Convert psi to Pa
    elif P_units != '':
        print("Unknown pressure unit. Assuming Pascal.")

    T_C, P_C, omega = get_substance_parameters(substance)

    if T_C and P_C and omega:
        a_val, b_val, A_val, B_val = calculate_parameters(T, T_C, P_C, omega, P)

        Z_roots = roots_of_Z(A_val, B_val)
        Z_max = max(Z_roots)
        print(f"\nFor {substance} at {T} K and {P} Pa:")
        print("Roots of Z:")
        for idx, root in enumerate(Z_roots, 1):
            print(f"{idx}. {root:.5f}")

        da_val = da_dT(T, T_C, P_C, omega)
        H_dep = enthalpy_departure(T, Z_max, B_val, a_val, da_val, b_val)
        S_dep = entropy_departure(T, Z_max, B_val, da_val, b_val)
        print(f"\nEnthalpy Departure: {H_dep:.2f} J/mol")
        print(f"Entropy Departure: {S_dep:.5f} J/(mol·K)")
    else:
        print(f"Data for {substance} not found in the database.")
