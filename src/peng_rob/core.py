import pandas as pd
import numpy as np
import sqlite3

R = 8.3144621  # Universal gas constant in J/(mol·K)

def kappa(omega):
    return 0.37464 + 1.54226 * omega - 0.26992 * omega**2

def alpha(T, T_C, omega):
    k = kappa(omega)
    return (1 + k * (1 - np.sqrt(T / T_C)))**2

def a(T, T_C, P_C, omega):
    return 0.45724 * (R * T_C)**2 * alpha(T, T_C, omega) / P_C

def da_dT(T, T_C, P_C, omega):
    k = kappa(omega)
    return -0.45724 * (R * T_C)**2 / P_C * k * (alpha(T, T_C, omega)/(T * T_C))**0.5

def b(T_C, P_C):
    return 0.07780 * R * T_C / P_C

def A(a_val, P, T):
    return a_val * P / (R * T)**2

def B(b_val, P, T):
    return b_val * P / (R * T)

def roots_of_Z(A_val, B_val):
    coefficients = [1, -(1-B_val), A_val - 2*B_val - 3*B_val**2, -A_val*B_val + B_val**2 + B_val**3]
    raw_roots = np.roots(coefficients)
    cleaned_roots = [root.real if abs(root.imag) < 1e-10 else root for root in raw_roots]
    return sorted(cleaned_roots, reverse=True)

def enthalpy_departure(T, Z, B, a_val, da_val, b_val):
    term1 = R * T * (Z - 1)
    term2 = (T * da_val - a_val) / (2 * np.sqrt(2) * b_val)
    term3 = np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B))
    return term1 + term2 * term3

def entropy_departure(T, Z, B, da_val, b_val):
    term1 = R * np.log(Z - B)
    term2 = da_val / (2 * np.sqrt(2) * b_val)
    term3 = np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B))
    return term1 + term2 * term3

def get_substance_parameters(substance):
    substance = substance.strip().lower()
    
    # Define the path to your SQLite database
    DB_PATH = "/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/db/properties_of_substances.db"
    
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch substance parameters from the database (case-insensitive lookup)
    cursor.execute("SELECT `T_(c)(K)`, `P_(c)(MPa)`, `omega` FROM substance_properties WHERE LOWER(`Substance`) = ?", (substance,))
    record = cursor.fetchone()

    conn.close()

    if record:
        T_C, P_C, omega = record
        P_C *= 1e6  # Convert to Pa
        return T_C, P_C, omega
    else:
        return None, None, None


def calculate_parameters(T, T_C, P_C, omega, P):
    a_val = a(T, T_C, P_C, omega)
    b_val = b(T_C, P_C)
    A_val = A(a_val, P, T)
    B_val = B(b_val, P, T)
    return a_val, b_val, A_val, B_val



