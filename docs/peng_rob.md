# Peng-Robinson Thermodynamic Calculations

This module provides a set of core functions for thermodynamic calculations using the Peng-Robinson equation of state.

---

## Functions

### `kappa(omega: float) -> float`

**Description**: 
Calculates the kappa value based on the acentric factor, \( \omega \).

**Parameters**:
- `omega`: The acentric factor of the substance.

**Returns**: 
The calculated kappa value.

**Example**:
```python
kappa_value = kappa(0.344)
```

---

### `alpha(T: float, T_C: float, omega: float) -> float`

**Description**: 
Calculates the alpha value based on the temperature, critical temperature, and acentric factor.

**Parameters**:
- `T`: Current temperature in Kelvin.
- `T_C`: Critical temperature of the substance.
- `omega`: Acentric factor of the substance.

**Returns**: 
The calculated alpha value.

---

### `a(T: float, T_C: float, P_C: float, omega: float) -> float`

**Description**: 
Calculates the "a" parameter for the Peng-Robinson equation based on the temperature, critical temperature, critical pressure, and acentric factor.

**Parameters**:
- `T`: Current temperature in Kelvin.
- `T_C`: Critical temperature of the substance.
- `P_C`: Critical pressure of the substance in Pa.
- `omega`: Acentric factor of the substance.

**Returns**: 
The calculated "a" parameter value.

---

### `da_dT(T: float, T_C: float, P_C: float, omega: float) -> float`

**Description**: 
Computes the temperature derivative of the "a" parameter in the Peng-Robinson equation.

**Parameters**:
- `T`: Current temperature in Kelvin.
- `T_C`: Critical temperature of the substance.
- `P_C`: Critical pressure of the substance in Pa.
- `omega`: Acentric factor of the substance.

**Returns**: 
The temperature derivative of the "a" parameter.

---

### `b(T_C: float, P_C: float) -> float`

**Description**: 
Calculates the "b" parameter for the Peng-Robinson equation using the critical temperature and pressure.

**Parameters**:
- `T_C`: Critical temperature of the substance.
- `P_C`: Critical pressure of the substance in Pa.

**Returns**: 
The calculated "b" parameter value.

---

### `A(a_val: float, P: float, T: float) -> float`

**Description**: 
Computes the "A" parameter for the Peng-Robinson equation based on the "a" parameter, pressure, and temperature.

**Parameters**:
- `a_val`: Value of the "a" parameter.
- `P`: Pressure in Pa.
- `T`: Temperature in Kelvin.

**Returns**: 
The computed "A" parameter value.

---

### `B(b_val: float, P: float, T: float) -> float`

**Description**: 
Computes the "B" parameter for the Peng-Robinson equation based on the "b" parameter, pressure, and temperature.

**Parameters**:
- `b_val`: Value of the "b" parameter.
- `P`: Pressure in Pa.
- `T`: Temperature in Kelvin.

**Returns**: 
The computed "B" parameter value.

---

### `roots_of_Z(A_val: float, B_val: float) -> List[float]`

**Description**: 
Solves for the roots of the compressibility factor equation in the Peng-Robinson equation of state.

**Parameters**:
- `A_val`: Value of the "A" parameter.
- `B_val`: Value of the "B" parameter.

**Returns**: 
A sorted list of roots representing potential compressibility factors.

---

### `enthalpy_departure(T: float, Z: float, B: float, a_val: float, da_val: float, b_val: float) -> float`

**Description**: 
Determines the departure enthalpy using the Peng-Robinson equation.

**Parameters**:
- `T`: Temperature in Kelvin.
- `Z`: Compressibility factor.
- `B`: "B" parameter value.
- `a_val`: "a" parameter value.
- `da_val`: Temperature derivative of the "a" parameter.
- `b_val`: "b" parameter value.

**Returns**: 
The computed departure enthalpy in J/mol.

---

### `entropy_departure(T: float, Z: float, B: float, da_val: float, b_val: float) -> float`

**Description**: 
Determines the departure entropy using the Peng-Robinson equation.

**Parameters**:
- `T`: Temperature in Kelvin.
- `Z`: Compressibility factor.
- `B`: "B" parameter value.
- `da_val`: Temperature derivative of the "a" parameter.
- `b_val`: "b" parameter value.

**Returns**: 
The computed departure entropy in J/(mol·K).

---

### `get_substance_parameters(substance: str) -> Tuple[float, float, float]`

**Description**: 
Fetches critical parameters and acentric factor of a given substance from the database.

**Parameters**:
- `substance`: Name of the substance.

**Returns**: 
A tuple containing the critical temperature (in Kelvin), critical pressure (in Pa), and acentric factor of the substance.

---

### `calculate_parameters(T: float, T_C: float, P_C: float, omega: float, P: float) -> Tuple[float, float, float, float]`

**Description**: 
Calculates thermodynamic parameters necessary for the Peng-Robinson equation.

**Parameters**:
- `T`: Temperature in Kelvin.
- `T_C`: Critical temperature of the substance.
- `P_C`: Critical pressure of the substance in Pa.
- `omega`: Acentric factor of the substance.
- `P`: Pressure in Pa.

**Returns**: 
A tuple containing the "a" parameter value, "b" parameter value, "A" parameter value, and "B" parameter value.

