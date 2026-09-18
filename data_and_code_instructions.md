# Data and Code Preparation Instructions

**Target AI/Assistant**: Use these instructions to generate the reproducible data and code package for the helium data/methods note
“Reproducible Reduced-Density-Matrix Descriptors for Helium Singlet and Triplet States.”
Do not restore the discarded title “Certified Electron Correlation in Helium: Exchange Dominates, Coulomb Loosens.”

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
├── LICENSE
├── README.md
├── requirements.txt
├── scripts/
│   ├── run_fci_he.py
│   ├── analyze_1rdm.py
│   ├── analyze_2rdm.py
│   ├── plot_intracule.py
│   └── test_identity.py
├── data/
│   ├── certified_qz.json
│   ├── intracule_curves.npz
│   ├── he_singlet_1rdm.json
│   ├── he_singlet_2rdm.json
│   ├── he_triplet_1rdm.json
│   └── he_triplet_2rdm.json
└── figures/
    ├── fig1_P_u_singlet_triplet.png
    ├── fig2_i_u_contact.png
    ├── fig3_mean_r12_vs_basis.png
    ├── intracule_comparison.png
    ├── intracule_contact.png
    ├── occupation_numbers.png
    └── r12_convergence.png
```

`lithium_fci_gpu_instructions.md` is an IDEA-0123 operator note. It is not part of the helium certificate and must stay out of the Zenodo deposit (`.zenodoignore`).

---

## Step 1: PySCF FCI Calculation Script

**File**: `scripts/run_fci_he.py`

**Task**: Write a PySCF script that:
1. Builds helium atom with aug-cc-pVQZ basis; remainder from the same aug-cc-pVTZ / aug-cc-pVQZ sequence;
2. Runs FCI for singlet (\(1^1S\)) and triplet (\(2^3S\));
3. Exports 1-RDM and 2-RDM to JSON files;
4. Prints occupation numbers and \(\langle r_{12}\rangle\).

Default export writes certified scalars only. Full AO tensors require `--run-fci` and are refused while IDEA-0123 holds the GPU.

**Key code snippets**:
```python
from pyscf import gto, scf, fci
import numpy as np
import json

# Build helium
mol = gto.M(atom='He 0 0 0', basis='aug-cc-pVQZ', verbose=4)

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
print("n_disc =", n[1])  # singlet: first occupation after HF filling (n[1]; triplet uses n[2])
```

**Output**: `natural_occupations.npy` and printed \(n_{\text{disc}}\).

---

## Step 3: 2-RDM Analysis Script

**File**: `scripts/analyze_2rdm.py`

**Task**: Diagonalize the occupied-block 2-RDM to get geminal occupation numbers. The pair matrix is \(G[(p,r),(q,s)]=\mathrm{transpose}(\mathrm{dm2},(0,2,1,3))\), then symmetrized. A naive `reshape(norb**2, norb**2)` without that transpose is the wrong map.

**Key code**:
```python
import numpy as np

dm2 = np.load('../data/he_singlet_2rdm.npy')
norb = dm2.shape[0]
g = np.transpose(np.asarray(dm2, dtype=float), (0, 2, 1, 3)).reshape(norb * norb, norb * norb)
g = 0.5 * (g + g.T)
lam = np.linalg.eigvalsh(g)[::-1]

np.save('../data/he_singlet_geminal_occupations.npy', lam)
print("Geminal occupations:", lam[:5])
print("Rank (lam > 1e-6):", np.sum(lam > 1e-6))
```

**Output**: `geminal_occupations.npy` and printed \(\lambda_k\).

---

## Step 4: Intracule Plotting Script

**File**: `scripts/plot_intracule.py`

**Task**: Plot certified helium intracules from `data/intracule_curves.npz` (IDEA-0121). Do not recompute the quadrature and do not use the GPU. Write both manuscript names (`fig1_…`, `fig2_…`, `fig3_…`) and the script names (`intracule_comparison.png`, `intracule_contact.png`, `r12_convergence.png`).

The live script in this directory is the implementation.

**Output**: the seven files listed under `figures/`.

---

## Step 5: README

**File**: `README.md`

The live `README.md` in this directory is authoritative. Do not regenerate a shorter template that reintroduces cc-pVQZ, PySCF v2.4, Windows default `python`, a different Zenodo DOI, or claims that full AO tensors are stored here.

Frozen labels: **aug-cc-pVQZ**, **PySCF v2.14.0**, remainder aug-cc-pVTZ/aug-cc-pVQZ. Interpreter: `/home/kai/.venvs/cuda-backends/bin/python`. Identity check: `scripts/test_identity.py`.

---

## Step 6: Requirements File

**File**: `requirements.txt`

**Content**:
```
pyscf==2.14.0
numpy>=1.21.0
matplotlib>=3.5.0
scipy>=1.7.0
```

---

## Step 7: GitHub and Zenodo

GitHub remote already exists: https://github.com/kaiplaketti/helium-correlation-data

1. Commit the working-tree corrections before publishing the Zenodo deposition. The current `HEAD` still has cc-pVQZ / PySCF v2.4 labels.
2. Keep the reserved draft DOI `10.5281/zenodo.22837641`. A 404 is expected until the deposition is published; do not replace the identifier.
3. After publication, the same DOI begins to resolve. Do not mint a second helium DOI for this snapshot.
4. Exclude `lithium_fci_gpu_instructions.md` and `STATUS.md` (see `.zenodoignore`).

---

## Notes for the AI

- Use **exact numbers** from the manuscript (e.g., \(n_{\text{disc}} = 0.007609\), \(\langle r_{12}\rangle = 1.424\) bohr, gate margins \(n_{\text{disc}}/(2\varepsilon) = 11.47\) and \(2.89\));
- Frozen software/basis: **PySCF v2.14.0**, **aug-cc-pVQZ**, remainder from aug-cc-pVTZ / aug-cc-pVQZ;
- \(n_{\text{disc}}\) is the first occupation after HF filling: singlet `n[1]`, triplet `n[2]`;
- The 2-RDM geminal map is `transpose(dm2, (0,2,1,3))`, not a naive reshape;
- This snapshot stores certified scalars and intracule curves, not full AO tensors;
- Ensure **reproducibility** (fixed random seeds, version-locked dependencies);
- Run `scripts/test_identity.py` (trace/occupation/contact identity on certified arrays).

---

**This completes the data and code package.** The AI should generate all files in the specified structure and ensure they run without errors.
