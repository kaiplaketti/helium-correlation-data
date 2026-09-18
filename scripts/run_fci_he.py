#!/usr/bin/env python3
"""Reproduce helium FCI 1-RDM/2-RDM export.

Default: do not run FCI. Certified QZ numbers already live in data/certified_qz.json.
Full FCI is CPU PySCF and must wait until IDEA-0123 releases the GPU/CPU intracule.

Interpreter: /home/kai/.venvs/cuda-backends/bin/python
Do not use Windows default python.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
CERT = DATA / "certified_qz.json"


def write_certified_arrays() -> None:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    np.save(DATA / "he_singlet_natural_occupations.npy", np.asarray(cert["singlet"]["leading_occupations"], dtype=float))
    np.save(DATA / "he_triplet_natural_occupations.npy", np.asarray(cert["triplet"]["leading_occupations"], dtype=float))
    np.save(
        DATA / "he_singlet_geminal_occupations.npy",
        np.asarray([cert["singlet"]["lambda_max"], cert["singlet"]["lambda_disc"]], dtype=float),
    )
    np.save(
        DATA / "he_triplet_geminal_occupations.npy",
        np.asarray([cert["triplet"]["lambda_max"], cert["triplet"]["lambda_disc"]], dtype=float),
    )
    for state in ("singlet", "triplet"):
        payload = {
            "state": state,
            "basis": cert["basis"],
            "1rdm_leading_occupations": cert[state]["leading_occupations"],
            "n_disc": cert[state]["n_disc"],
            "2rdm_lambda_max": cert[state]["lambda_max"],
            "2rdm_lambda_disc": cert[state]["lambda_disc"],
            "mean_r12_gamma": cert[state]["mean_r12_gamma"],
            "note": "Full AO tensors are produced only by --run-fci.",
        }
        (DATA / f"he_{state}_1rdm.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        (DATA / f"he_{state}_2rdm.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("Wrote certified occupation arrays and JSON summaries to", DATA)


def run_fci(basis: str) -> None:
    from pyscf import ao2mo, fci, gto, scf
    from pyscf.fci import direct_spin1

    DATA.mkdir(exist_ok=True)
    mol = gto.M(atom="He 0 0 0", basis=basis, unit="Bohr", charge=0, spin=0, symmetry=False, verbose=0)
    mf = scf.RHF(mol)
    mf.conv_tol = 1.0e-12
    mf.kernel()
    coeff = np.asarray(mf.mo_coeff, dtype=float)
    norb = int(coeff.shape[1])
    h1 = coeff.T @ (mol.intor("int1e_kin") + mol.intor("int1e_nuc")) @ coeff
    eri = ao2mo.restore(1, ao2mo.full(mol, coeff), norb)
    solver = fci.direct_spin1.FCI()
    solver.conv_tol = 1.0e-10
    for state, nelec, spin in (("singlet", (1, 1), 0), ("triplet", (2, 0), 2)):
        solver.spin = spin
        energy, ci = solver.kernel(h1, eri, norb, nelec)
        s2, _ = solver.spin_square(ci, norb, nelec)
        dm1 = np.asarray(direct_spin1.make_rdm1(ci, norb, nelec), dtype=float)
        (dm1a, dm1b), (dm2aa, dm2ab, dm2bb) = direct_spin1.make_rdm12s(ci, norb, nelec)
        np.save(DATA / f"he_{state}_1rdm.npy", dm1)
        occupied = np.asarray(dm2ab if state == "singlet" else dm2aa, dtype=float)
        np.save(DATA / f"he_{state}_2rdm.npy", occupied)
        occ = np.sort(np.linalg.eigvalsh(0.5 * (dm1 + dm1.T)))[::-1]
        print(
            json.dumps(
                {
                    "state": state,
                    "energy": float(energy),
                    "s2": float(s2),
                    "norb": norb,
                    "n_max": float(occ[0]),
                    "n_disc": float(occ[1] if state == "singlet" else occ[2]),
                    "trace_1rdm": float(np.trace(dm1)),
                }
            ),
            flush=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-fci",
        action="store_true",
        help="Run helium FCI. Forbidden while IDEA-0123 holds the GPU. Default exports certified arrays only.",
    )
    parser.add_argument("--basis", default="aug-cc-pvqz")
    args = parser.parse_args()
    DATA.mkdir(exist_ok=True)
    write_certified_arrays()
    if args.run_fci:
        if os.environ.get("IDEA0123_GPU_ACTIVE", "1") == "1":
            print(
                "Refusing --run-fci: IDEA-0123 currently holds GPU/CPU. "
                "Rerun with IDEA0123_GPU_ACTIVE=0 after that reservation is COMPLETE.",
                file=sys.stderr,
            )
            raise SystemExit(2)
        run_fci(args.basis)


if __name__ == "__main__":
    main()
