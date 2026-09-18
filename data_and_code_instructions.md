# Data and Code Preparation Instructions

**Target AI/Assistant**: Use these instructions to generate the reproducible data and code package for the helium correlation manuscript.

---

## Overview

We need to produce:
1. **FCI 1-RDM and 2-RDM data files** (JSON or HDF5);
2. **PySCF scripts** to reproduce the calculations;
3. **Plotting scripts** for intracule and occupation numbers;
4. **README** with usage instructions.

All files should be organized in a GitHub-ready structure.

---

## Directory Structure

```
helium-correlation-data/
├── README.md
├── requirements.txt
├── scripts/
│   ├── run_fci_he.py
│   ├── analyze_1rdm.py
│   ├── analyze_2rdm.py
│   └── plot_intracule.py
├── data/
│   ├── he_singlet_1rdm.json
│   ├── he_singlet_2rdm.json
│   ├── he_triplet_1rdm.json
│   └── he_triplet_2rdm.json
└── figures/
    ├── intracule_comparison.png
    ├── occupation_numbers.png
    └── r12_convergence.png
```

---

## Step 1: PySCF FCI Calculation Script

**File**: `scripts/run_fci_he.py`

**Task**: Write a PySCF script that:
1. Builds helium atom with cc-pVQZ basis;
2. Runs FCI for singlet (\(1^1S\)) and triplet (\(2^3S\));
3. Exports 1-RDM and 2-RDM to JSON files;
4. Prints occupation numbers and \(\langle r_{12}\rangle\).

**Key code snippets**:
```python
from pyscf import gto, scf, fci
import numpy as np
import json

# Build helium
mol = gto.M(atom='He 0 0 0', basis='cc-pVQZ', verbose=4)

# Hartree-Fock
mf = scf.RHF(mol).run()

# FCI singlet
ci_singlet = fci.FCI(mf)
ci_singlet.spin = 0  # S=0
ci_singlet.verbose = 4
e_singlet, ci_singlet_vec = ci_singlet.kernel()

# Export 1-RDM
dm1_singlet = ci_singlet.make_rdm1(ci_singlet_vec, ci_singlet.norb, ci_singlet.nelec)
np.save('../data/he_singlet_1rdm.npy', dm1_singlet)

# Export 2-RDM (spin-summed)
dm2_singlet = ci_singlet.make_rdm2(ci_singlet_vec, ci_singlet.norb, ci_singlet.nelec)
np.save('../data/he_singlet_2rdm.npy', dm2_singlet)

# Repeat for triplet (spin=2, S=1)
```

**Output**: `.npy` files for 1-RDM and 2-RDM.

---

## Step 2: 1-RDM Analysis Script

**File**: `scripts/analyze_1rdm.py`

**Task**: Diagonalize 1-RDM and compute occupation numbers.

**Key code**:
```python
import numpy as np

# Load 1-RDM
dm1 = np.load('../data/he_singlet_1rdm.npy')

# Diagonalize
n, c = np.linalg.eigh(dm1)

# Sort descending
idx = np.argsort(n)[::-1]
n = n[idx]

# Save occupation numbers
np.save('../data/he_singlet_natural_occupations.npy', n)

# Print
print("Natural occupations:", n[:10])
print("n_disc =", n[2])  # First virtual
```

**Output**: `natural_occupations.npy` and printed \(n_{\text{disc}}\).

---

## Step 3: 2-RDM Analysis Script

**File**: `scripts/analyze_2rdm.py`

**Task**: Diagonalize 2-RDM to get geminal occupation numbers.

**Key code**:
```python
import numpy as np

# Load 2-RDM (shape: norb×norb×norb×norb)
dm2 = np.load('../data/he_singlet_2rdm.npy')

# Reshape to matrix (norb² × norb²)
norb = dm2.shape[0]
dm2_mat = dm2.reshape(norb**2, norb**2)

# Diagonalize
lam, phi = np.linalg.eigh(dm2_mat)

# Sort descending
idx = np.argsort(lam)[::-1]
lam = lam[idx]

# Save geminal occupations
np.save('../data/he_singlet_geminal_occupations.npy', lam)

# Print
print("Geminal occupations:", lam[:5])
print("Rank (lam > 1e-6):", np.sum(lam > 1e-6))
```

**Output**: `geminal_occupations.npy` and printed \(\lambda_k\).

---

## Step 4: Intracule Plotting Script

**File**: `scripts/plot_intracule.py`

**Task**: Compute and plot \(I(r_{12})\) from the leading geminal.

**Key code**:
```python
import numpy as np
import matplotlib.pyplot as plt

# Load leading geminal (from phi[:, 0] reshaped)
phi_max = np.load('../data/he_singlet_geminal_phi_max.npy')  # Shape: norb×norb

# Compute intracule on grid
r_grid = np.linspace(0, 10, 500)
I_r = []

for r in r_grid:
    # Integrate |phi_max(r1, r2)|² delta(|r1-r2| - r)
    # Simplified: use spherical average
    I_val = compute_intracule_at_r(phi_max, r)  # Implement this
    I_r.append(I_val)

# Plot
plt.plot(r_grid, I_r, label='Singlet')
plt.xlabel(r'$r_{12}$ (bohr)')
plt.ylabel(r'$I(r_{12})$')
plt.legend()
plt.savefig('../figures/intracule_comparison.png')
```

**Output**: `intracule_comparison.png`.

---

## Step 5: README

**File**: `README.md`

**Content**:
```markdown
# Helium Correlation Data and Code

This repository contains the FCI 1-RDM and 2-RDM data, analysis scripts, and plotting code for the manuscript "Certified Electron Correlation in Helium: Exchange Dominates, Coulomb Loosens."

## Requirements

- Python 3.9+
- PySCF v2.4
- NumPy
- Matplotlib

Install with:
```bash
pip install -r requirements.txt
```

## Usage

1. Run FCI calculations:
   ```bash
   cd scripts
   python run_fci_he.py
   ```

2. Analyze 1-RDM:
   ```bash
   python analyze_1rdm.py
   ```

3. Analyze 2-RDM:
   ```bash
   python analyze_2rdm.py
   ```

4. Plot intracule:
   ```bash
   python plot_intracule.py
   ```

## Data Files

- `data/he_singlet_1rdm.npy`: Singlet 1-RDM
- `data/he_singlet_2rdm.npy`: Singlet 2-RDM
- `data/he_triplet_1rdm.npy`: Triplet 1-RDM
- `data/he_triplet_2rdm.npy`: Triplet 2-RDM

## Figures

- `figures/intracule_comparison.png`: Intracule for singlet and triplet
- `figures/occupation_numbers.png`: Natural occupation numbers
- `figures/r12_convergence.png`: \(\langle r_{12}\rangle\) vs. basis set

## License

MIT License
```

---

## Step 6: Requirements File

**File**: `requirements.txt`

**Content**:
```
pyscf==2.4.0
numpy>=1.21.0
matplotlib>=3.5.0
scipy>=1.7.0
```

---

## Step 7: GitHub and Zenodo

1. **Create GitHub repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial helium correlation data"
   git remote add origin https://github.com/yourusername/helium-correlation-data.git
   git push -u origin main
   ```

2. **Archive on Zenodo** (for DOI):
   - Go to https://zenodo.org
   - Link GitHub repository
   - Create new version
   - Get DOI (e.g., `10.5281/zenodo.XXXXXXX`)

3. **Update manuscript** with:
   - GitHub link
   - Zenodo DOI

---

## Notes for the AI

- Use **exact numbers** from the manuscript (e.g., \(n_{\text{disc}} = 0.007609\), \(\langle r_{12}\rangle = 1.424\) bohr);
- Ensure **reproducibility** (fixed random seeds, version-locked dependencies);
- Add **unit tests** if possible (e.g., check trace of 1-RDM = 2);
- Include **Jupyter notebook** version for interactive exploration (optional).

---

**This completes the data and code package.** The AI should generate all files in the specified structure and ensure they run without errors.