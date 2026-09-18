# Lithium FCI on GPU — execution notes

EI TESTAA AKTIIVISTA QPHI-MALLIA.

This file is the operator note for IDEA-0123. The frozen scientific package is

`research/idea0123_li_n3_pair_cumulant_intracule_gate_2026-09-18`

not a separate GitHub sidecar.

## What this run does

1. Lithium atom, ground \(^2S\), `nelec=(2,1)`, cc-pVTZ first, then cc-pVDZ remainder, then cc-pVQZ if memory allows.
2. CPU Davidson FCI in WSL PySCF 2.14. `gpu4pyscf` is **not** installed and is not required: dense FCI is three-electron and already cheap; the GPU work is the full ab 2-RDM intracule contraction.
3. Export/analyze 1-RDM occupations, ab 2-RDM geminal occupations, full-Γ intracule, 1-RDM-wedge intracule, and the pair cumulant \(\Delta=\Gamma-\gamma\wedge\gamma\).
4. Frozen gates: rank \(>1\), \(n_{\mathrm{disc}}>2\varepsilon\), Coulomb-contact depletion \(i_{\mathrm{wedge}}(0)-i_\Gamma(0)>2\varepsilon\).
5. Reported but not a moved pass gate: is \(\delta_c<0\) like helium (\(\delta_c=-0.056\))?

## Environment

```bat
wsl.exe -e /home/kai/.venvs/cuda-backends/bin/python /mnt/c/Users/kaipl/Documents/ChatGPT/Atomi/research/idea0123_li_n3_pair_cumulant_intracule_gate_2026-09-18/run_li_n3_cumulant.py calibrate
```

- Interpreter: `/home/kai/.venvs/cuda-backends/bin/python`
- PySCF 2.14.0 (CPU FCI)
- CuPy 14.2.0 on RTX 3060 Laptop 6 GiB
- Do not use Windows default `python`

## Expected order of magnitude (not gates)

- \(n_{1s}\approx 1.98\)
- \(n_{2s}\approx 0.98\)
- \(n_{\mathrm{disc}}\approx 0.02\)

## Troubleshooting

- GPU not seen: the script records `CUPY_FAIL` and falls back to CPU intracule.
- Out of memory: QZ is labelled `NOT_RUN_RESOURCE`; TZ/DZ remainder is still a valid coarser certificate.
- `gpu4pyscf` missing: not a scientific failure. FCI stays on CPU.

## What this is not

- Not a test of `QPHI_DENSITY_SCATTERING_V1` or `ANGULAR_MULTIPOLE_ATOMIC_WAVE_V1`.
- Not lithium \(^2P\) (that is IDEA-0124).
- Not a reopen of IDEA-0104.
