#!/usr/bin/env python3
"""Identity checks on certified helium numbers. No FCI, no GPU."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    cert = json.loads((DATA / "certified_qz.json").read_text(encoding="utf-8"))
    ns = np.load(DATA / "he_singlet_natural_occupations.npy")
    nt = np.load(DATA / "he_triplet_natural_occupations.npy")
    assert abs(float(ns[0]) - cert["singlet"]["n_max"]) < 1e-12
    assert abs(float(ns[1]) - 0.007608570565326827) < 1e-12
    assert abs(float(nt[2]) - cert["triplet"]["n_disc"]) < 1e-12
    gs = np.load(DATA / "he_singlet_geminal_occupations.npy")
    gt = np.load(DATA / "he_triplet_geminal_occupations.npy")
    assert abs(float(gs[0]) - 1.0) < 1e-12
    assert float(gs[1]) < 1e-12
    assert abs(float(gt[0]) - 2.0) < 1e-12
    assert cert["singlet"]["delta_c"] < 0.0
    assert abs(cert["singlet"]["mean_r12_gamma"] - 1.4237744544548225) < 1e-12
    assert abs(cert["triplet"]["mean_r12_gamma"] - 4.090048887717378) < 1e-12
    curves = np.load(DATA / "intracule_curves.npz")
    assert curves["i_gamma_s"][0] > 0.1
    assert curves["i_gamma_t"][0] < 1e-20
    print("identity PASS")


if __name__ == "__main__":
    main()
