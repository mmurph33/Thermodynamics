import contextlib
import pandas as pd
import numpy as np
import sqlite3
from scipy.optimize import root_scalar

R = 8.3144621  # Universal gas constant in J/(mol·K)
DB_PATH = "/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/db/properties_of_substances.db"

class PengRobinsonEOS:
    """Class containing methods for Peng-Robinson Equation of State calculations."""
    
    @staticmethod
    def kappa(omega):
        """Calculate kappa value based on acentric factor."""
        return 0.37464 + 1.54226 * omega - 0.26992 * omega**2

    @staticmethod
    def alpha(T, T_C, omega):
        """Calculate alpha value."""
        k = PengRobinsonEOS.kappa(omega)
        return (1 + k * (1 - np.sqrt(T / T_C)))**2

    @staticmethod
    def a(T, T_C, P_C, omega):
        """Calculate 'a' value for Peng-Robinson EOS."""
        return 0.45724 * (R * T_C)**2 * PengRobinsonEOS.alpha(T, T_C, omega) / P_C

    @staticmethod
    def da_dT(T, T_C, P_C, omega):
        """Calculate derivative of 'a' with respect to temperature."""
        k = PengRobinsonEOS.kappa(omega)
        return -0.45724 * (R * T_C)**2 / P_C * k * (PengRobinsonEOS.alpha(T, T_C, omega)/(T * T_C))**0.5

    @staticmethod
    def b(T_C, P_C):
        """Calculate 'b' value for Peng-Robinson EOS."""
        return 0.07780 * R * T_C / P_C

    @staticmethod
    def A(a_val, P, T):
        """Calculate 'A' value."""
        return a_val * P / (R * T)**2

    @staticmethod
    def B(b_val, P, T):
        """Calculate 'B' value."""
        return b_val * P / (R * T)

    
    @staticmethod
    def compressibility_factor_eq(Z, A_val, B_val):
        """Equation for compressibility factor Z."""
        return Z**3 - (1 - B_val) * Z**2 + (A_val - 3 * B_val**2 - 2 * B_val) * Z - (A_val * B_val - B_val**2 - B_val**3)
    
    @staticmethod
    def roots_of_Z(A_val, B_val):
        """Calculate the roots of the compressibility factor equation using scipy."""
        roots = []
        for method in ['bisect', 'ridder', 'brentq']:
            with contextlib.suppress(Exception):
                root = root_scalar(PengRobinsonEOS.compressibility_factor_eq, args=(A_val, B_val), bracket=[0, 4], method=method)
                roots.append(root.root)
        return sorted(list(set(roots)), reverse=True)


class DatabaseHandler:
    """Class for handling database operations."""

    @staticmethod
    def get_substance_parameters(substance):
        """Fetch substance parameters from the database."""
        substance = substance.strip().lower()
        
        # Connect to the SQLite database
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Fetch substance parameters (case-insensitive lookup)
            cursor.execute("SELECT `T_(c)(K)`, `P_(c)(MPa)`, `omega` FROM substance_properties WHERE LOWER(`Substance`) = ?", (substance,))
            record = cursor.fetchone()

        if record:
            T_C, P_C, omega = record
            P_C *= 1e6  # Convert to Pa
            return T_C, P_C, omega
        else:
            return None, None, None

def calculate_parameters(T, T_C, P_C, omega, P):
    """Calculate thermodynamic parameters."""
    a_val = PengRobinsonEOS.a(T, T_C, P_C, omega)
    b_val = PengRobinsonEOS.b(T_C, P_C)
    A_val = PengRobinsonEOS.A(a_val, P, T)
    B_val = PengRobinsonEOS.B(b_val, P, T)
    return a_val, b_val, A_val, B_val
