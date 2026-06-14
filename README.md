# DLM Aerodynamic Mesh Generator (Panel & Aileron)

> **Code originally developed by Prane (2025).**

This Python script automates the generation and discretization of two-dimensional aerodynamic meshes for the **Doublet Lattice Method (DLM)** used in aeroelastic analyses. Its main focus is to maintain perfect physical continuity between two consecutive sections (Fore Panel and Aft Panel/Aileron), allowing strategic node refinement via sine/cosine laws.

---

## What Does the Code Do?

1. **Calculates the Real Proportion:** Divides the requested number of panels based on the actual physical dimensions of the chords (`corda_frente` and `corda_tras`).
2. **Refines the Edges:** Applies mathematical transformations to "squeeze" the panels close to the junction and the Trailing Edge (TE), ensuring higher accuracy where air flow changes abruptly.
3. **Unifies and Normalizes:** Joins both blocks into a continuous "Full Panel" that scales perfectly from `0.000000` (Leading Edge) to `1.000000` (Trailing Edge).
4. **Exports Everything to Excel:** Generates an `.xlsx` file locked to 6 decimal places, ready to be copied or imported into your aeroelasticity software.

---

## How to Use (Step-by-Step)

### 1. Prerequisites and Dependencies
The code requires the `numpy`, `pandas`, and `xlsxwriter` libraries. 
* **Automatic Installation:** The first time you run it, the script itself will detect if anything is missing and ask in the terminal if you want to install it automatically (`[Y/N]`).
* **Manual Installation:** If you prefer to do it yourself via the terminal:
  ```bash
  pip install numpy pandas xlsxwriter

---

### 2. Configuring the Variables 
Open the script and scrool to the end, under the `CONFIGURAÇÕES INICIAIS`
