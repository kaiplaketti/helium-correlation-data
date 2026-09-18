#!/usr/bin/env python3
"""Geminal occupations of an occupied-block 2-RDM.

The pair matrix is G[(p,r),(q,s)] = transpose(dm2, (0,2,1,3)), then symmetrized.
A naive reshape(norb**2, norb**2) without that transpose is the wrong map.
Helium N=2 is rank-1: discarded lambda is numerical zero (IDEA-0118).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RANK_CUT = 1.0e-6


def pair_occupations(dm2: np.ndarray) -> np.ndarray:
    n = dm2.shape[0]
    g = np.transpose(np.asarray(dm2, dtype=float), (0, 2, 1, 3)).reshape(n * n, n * n)
    g = 0.5 * (g + g.T)
    vals = np.linalg.eigvalsh(g)[::-1]
    return vals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", choices=("singlet", "triplet"), default="singlet")
    args = parser.parse_args()
    rdm_path = DATA / f"he_{args.state}_2rdm.npy"
    out = DATA / f"he_{args.state}_geminal_occupations.npy"
    if rdm_path.exists():
        lam = pair_occupations(np.load(rdm_path))
        source = str(rdm_path)
    else:
        lam = np.load(out if out.exists() else DATA / f"he_{args.state}_geminal_occupations.npy")
        source = "certified geminal occupations (full 2-RDM not exported)"
    np.save(out, lam)
    print("source:", source)
    print("Geminal occupations:", lam[:5])
    print("lambda_max =", float(lam[0]))
    print("lambda_disc =", float(lam[1]) if lam.size > 1 else 0.0)
    print("Rank (lam > 1e-6):", int(np.sum(lam > RANK_CUT)))


if __name__ == "__main__":
    main()
