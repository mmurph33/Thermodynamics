# Thermodynamics_Assistant
Thermodynamics Helper Program

## Peng-Robinson Module

The Peng-Robinson module in Thermodynamics_Assistant provides a set of functions to calculate thermodynamic properties using the Peng-Robinson equation of state. This module aids in the determination of various parameters such as compressibility factor, enthalpy departure, entropy departure, and more for a given substance under specific conditions.

### Features:

- Calculation of various thermodynamic parameters using the Peng-Robinson equation of state.
- Fetches substance-specific parameters like critical temperature, critical pressure, and acentric factor from a database.
- Ability to handle different units for temperature and pressure.
- Comprehensive documentation available in `docs/peng_rob.md`.

### How to use:

1. Ensure that the SQLite database containing substance properties is correctly set up.
2. Use the script `scripts/peng_rob_tool.py` to interactively get results for a specific substance, temperature, and pressure.

For a detailed breakdown of each function and its usage, refer to the [Peng-Robinson Documentation](./docs/peng_rob.md).
