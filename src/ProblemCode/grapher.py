import contextlib
import pandas as pd
import numpy as np
import sqlite3
from scipy.optimize import root_scalar
from core import DatabaseHandler

R = 8.3144621  # Universal gas constant in J/(mol·K)
DB_PATH = "/Users/mattmurphy/Thermodynamics_Assistant/ChemE_Helper_Program/db/properties_of_substances.db"

# Universal gas constant in J/(mol·K)
def __init__(self, substance_name):
    db_handler = DatabaseHandler(DB_PATH)
    substance = db_handler.get_substance(substance_name)
    self.Tc = substance['Tc']
    self.Pc = substance['Pc']
    self.omega = substance['omega']

def kappa_pr(self):
    """Calculate kappa based on the acentric factor."""
    return 0.37464 + 1.54226 * self.omega - 0.26993 * self.omega**2

def alpha_pr(self, T):
    """Calculate alpha parameter for the Peng-Robinson EOS."""
    return (1 + self.kappa_pr() * (1 - (T / self.Tc)**0.5))**2

def apr(self, T):
    """Calculate the attraction parameter 'a'."""
    return self.acpr() * self.alpha_pr(T)

def bpr(self):
    """Calculate the co-volume 'b' for the Peng-Robinson EOS."""
    return 0.07779607 * (self.R * self.Tc / self.Pc)

def Ppr(self, T, v):
    """Implement the Peng-Robinson equation of state."""
    a = self.apr(T)
    b = self.bpr()
    return (self.R * T / v - b) - (a / (v**2 * (1 + 2 * (b / v) - ((b / v)**2))))

def acpr(self):
    """Calculate the critical molecular attraction parameter."""
    return 0.45723553 * (self.R * self.Tc)**2 / self.Pc