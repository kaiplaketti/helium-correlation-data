#!/usr/bin/env python3
"""Diagonalize a helium 1-RDM or print certified natural occupations.

n_disc is the first occupation after the HF filled count:
singlet filled=1 so n_disc = n[1]; triplet filled=2 so n_disc = n[2].
The instruction-file index n[2] for the singlet is incorrect.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
HF_FILLED = {"singlet": 1, "triplet": 2}


def occupations_from_rdm(path: Path) -> np.ndarray:
    dm1 = np.load(path)
    vals = np.linalg.eigvalsh(0.5 * (dm1 + dm1.T))
    return vals[::-1].copy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", choices=("singlet", "triplet"), default="singlet")
    args = parser.parse_args()
    rdm_path = DATA / f"he_{args.state}_1rdm.npy"
    if rdm_path.exists():
        occ = occupations_from_rdm(rdm_path)
        source = str(rdm_path)
        trace = float(occ.sum())
    else:
        occ = np.load(DATA / f"he_{args.state}_natural_occupations.npy")
        source = "certified leading occupations (full 1-RDM not exported)"
        cert = json.loads((DATA / "certified_qz.json").read_text(encoding="utf-8"))
        trace = float(np.sum(cert[args.state]["leading_occupations"]))
    filled = HF_FILLED[args.state]
    n_disc = float(occ[filled]) if occ.size > filled else float("nan")
    out = DATA / f"he_{args.state}_natural_occupations.npy"
    np.save(out, occ)
    print("source:", source)
    print("Natural occupations:", occ[:10])
    print(f"n_max = {float(occ[0]):.12f}")
    print(f"n_disc (index {filled}) = {n_disc:.12e}")
    print(f"leading-sum (not always N_e if truncated) = {trace:.12f}")
    if rdm_path.exists() and abs(float(occ.sum()) - 2.0) > 1.0e-8:
        raise SystemExit("1-RDM trace gate failed")


if __name__ == "__main__":
    main()
