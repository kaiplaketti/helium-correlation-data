# Helium Correlation Data and Code

EI TESTAA AKTIIVISTA QPHI-MALLIA.

Local reproducible package for the draft
“Certified Electron Correlation in Helium: Exchange Dominates, Coulomb Loosens.”
It is a quantitative FCI certificate, not a formation law and not new physics.

Certified numbers come from IDEA-0116 (1-RDM), IDEA-0118 (geminals),
IDEA-0119 (leading-geminal intracule) and IDEA-0121 (pair cumulant).
The frozen basis is **aug-cc-pVQZ**, PySCF **2.14.0**. The manuscript draft’s
`cc-pVQZ` / PySCF 2.4 labels are outdated.

IDEA-0123 (lithium N=3) holds the GPU. This package does **not** rerun helium
FCI until that reservation is `COMPLETE`.

## Requirements

- Python 3.12 (WSL research interpreter: `/home/kai/.venvs/cuda-backends/bin/python`)
- NumPy, Matplotlib, SciPy
- PySCF 2.14 only if you pass `--run-fci`

```bash
pip install -r requirements.txt
```

Do not use Windows default `python`.

## Usage

From this directory, with the WSL interpreter:

```bash
/home/kai/.venvs/cuda-backends/bin/python scripts/run_fci_he.py
/home/kai/.venvs/cuda-backends/bin/python scripts/analyze_1rdm.py --state singlet
/home/kai/.venvs/cuda-backends/bin/python scripts/analyze_1rdm.py --state triplet
/home/kai/.venvs/cuda-backends/bin/python scripts/analyze_2rdm.py --state singlet
/home/kai/.venvs/cuda-backends/bin/python scripts/analyze_2rdm.py --state triplet
/home/kai/.venvs/cuda-backends/bin/python scripts/plot_intracule.py
/home/kai/.venvs/cuda-backends/bin/python scripts/test_identity.py
```

Full AO 1-RDM/2-RDM tensors are written only by:

```bash
IDEA0123_GPU_ACTIVE=0 /home/kai/.venvs/cuda-backends/bin/python scripts/run_fci_he.py --run-fci
```

That flag is refused while IDEA-0123 is active.

## Certified QZ numbers

| | singlet | triplet |
|---|---|---|
| \(n_{\max}\) | 1.983889 | 0.999618 |
| \(n_{\mathrm{disc}}\) | 0.007609 | 0.000125 |
| \(\langle r_{12}\rangle_\Gamma\) / bohr | 1.4238 | 4.0900 |
| \(\langle r_{12}\rangle_{\gamma\wedge\gamma}\) / bohr | 1.3676 | 4.0748 |
| \(\delta_c\) / bohr | −0.0562 | −0.0153 |
| \(i_\Gamma(0)\) | 0.1245 | ~0 |
| geminal rank | 1 | 1 |

Exchange fraction \(f_x=1.015\). Coulomb loosens the singlet versus the 1-RDM
wedge. The singlet–triplet split is already in that wedge.

## Data files

- `data/certified_qz.json`: all frozen scalars and TZ/DZ means
- `data/intracule_curves.npz`: \(P(u)\) and \(i(u)\) for \(\Gamma\) and the wedge
- `data/he_*_natural_occupations.npy`, `he_*_geminal_occupations.npy`
- `data/he_*_1rdm.json`, `he_*_2rdm.json`: summaries; full tensors only after `--run-fci`

## Figures

- `figures/intracule_comparison.png`
- `figures/intracule_contact.png`
- `figures/occupation_numbers.png`
- `figures/r12_convergence.png`

## Analysis notes

- Singlet \(n_{\mathrm{disc}}\) is occupation index **1**, not 2.
- The 2-RDM geminal map is `transpose(dm2, (0,2,1,3))`, not a naive reshape.
- Rank-1 2-RDM is an N=2 identity (IDEA-0118), not a correlation failure.

## GitHub / Zenodo

Not published. Do not invent a DOI. Keep this tree local until a remote is
created on purpose.

## License

MIT, when published. Until then this is a local research snapshot.
