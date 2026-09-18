# Helium Correlation Data and Code

EI TESTAA AKTIIVISTA QPHI-MALLIA.

Open FCI package for the draft
“Reproducible Reduced-Density-Matrix Descriptors for Helium Singlet and Triplet States.”
It is a finite-basis implementation of known helium pair-structure features,
not a new mechanism and not a Hylleraas/Pekeris-class benchmark.

Certified numbers come from IDEA-0116 (1-RDM), IDEA-0118 (geminals),
IDEA-0119 (leading-geminal intracule) and IDEA-0121 (pair cumulant).
The frozen basis is **aug-cc-pVQZ**, PySCF **2.14.0**. The manuscript
uses the same labels.

Full AO tensors are not in this release. Do not rerun helium FCI while
another GPU job holds the machine.

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

That flag is refused while a conflicting GPU/CPU job is active.

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

Exchange-containing \(\gamma\wedge\gamma\) already holds most of the reported
mean-distance difference between \(1\,^1S\) and \(2\,^3S\); \(\delta_c\) is a
smaller correction on that descriptor.

## Data files

- `data/certified_qz.json`: all frozen scalars and TZ/DZ means
- `data/intracule_curves.npz`: \(P(u)\) and \(i(u)\) for \(\Gamma\) and the wedge
- `data/he_*_natural_occupations.npy`, `he_*_geminal_occupations.npy`
- `data/he_*_1rdm.json`, `he_*_2rdm.json`: summaries; full tensors only after `--run-fci`

## Figures

Manuscript figures (kept under both names; same plots):

| Manuscript | File | Also written by `plot_intracule.py` |
|---|---|---|
| Fig. 1 \(P(u)\) | `figures/fig1_P_u_singlet_triplet.png` | `intracule_comparison.png` |
| Fig. 2 coalescence | `figures/fig2_i_u_contact.png` | `intracule_contact.png` |
| Fig. 3 \(\langle r_{12}\rangle\) vs basis | `figures/fig3_mean_r12_vs_basis.png` | `r12_convergence.png` |

`figures/occupation_numbers.png` is an extra natural-occupation bar plot.

## Analysis notes

- Singlet \(n_{\mathrm{disc}}\) is occupation index **1**, not 2. Triplet uses index **2**.
- The 2-RDM geminal map is `transpose(dm2, (0,2,1,3))`, not a naive reshape.
- Rank-1 2-RDM is an N=2 identity (IDEA-0118), not a correlation failure.

## What is not in this helium deposit

- Full AO 1-RDM/2-RDM tensors (summaries only until `--run-fci` is allowed).
- `lithium_fci_gpu_instructions.md` is an IDEA-0123 operator note, not helium evidence. Exclude it from Zenodo (see `.zenodoignore`).

## GitHub / Zenodo

- GitHub: https://github.com/kaiplaketti/helium-correlation-data
- Reserved Zenodo draft DOI: https://doi.org/10.5281/zenodo.22837641
- A 404 from `doi.org` is expected until the deposition is published from a
  tagged snapshot. Do not replace the identifier.
- Publish Zenodo only after this rewritten data/methods note is the single
  manuscript in the tagged tree.

## License

Scripts: MIT. Data, figures, and documentation: CC BY 4.0 where `LICENSE-DATA` is present. See `LICENSE-CODE` and `LICENSE-DATA` on the published branch.
