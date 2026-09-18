#!/usr/bin/env python3
"""Plot certified helium intracules, occupations, and mean-r12 convergence.

Curves come from IDEA-0121 INTRACULE_CURVES.npz (copied to data/intracule_curves.npz).
This does not recompute the quadrature and does not use the GPU.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
CERT = json.loads((DATA / "certified_qz.json").read_text(encoding="utf-8"))


def main() -> None:
    FIG.mkdir(exist_ok=True)
    curves = np.load(DATA / "intracule_curves.npz")
    u = np.asarray(curves["u"], dtype=float)
    p_s = np.asarray(curves["p_gamma_s"], dtype=float)
    p_t = np.asarray(curves["p_gamma_t"], dtype=float)
    p_ws = np.asarray(curves["p_wedge_s"], dtype=float)
    p_wt = np.asarray(curves["p_wedge_t"], dtype=float)
    i_s = np.asarray(curves["i_gamma_s"], dtype=float)
    i_t = np.asarray(curves["i_gamma_t"], dtype=float)
    i_ws = np.asarray(curves["i_wedge_s"], dtype=float)
    i_wt = np.asarray(curves["i_wedge_t"], dtype=float)

    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.plot(u, p_s, color="#b00020", lw=2.0, label=r"singlet $P_\Gamma$")
    ax.plot(u, p_t, color="#1f4e79", lw=2.0, label=r"triplet $P_\Gamma$")
    ax.plot(u, p_ws, color="#b00020", lw=1.2, ls="--", label=r"singlet $P_{\gamma\wedge\gamma}$")
    ax.plot(u, p_wt, color="#1f4e79", lw=1.2, ls="--", label=r"triplet $P_{\gamma\wedge\gamma}$")
    ax.set_xlim(0, 8)
    ax.set_xlabel(r"$u=r_{12}$ (bohr)")
    ax.set_ylabel(r"$P(u)$ (bohr$^{-1}$)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Helium FCI geminal intracule, aug-cc-pVQZ")
    fig.tight_layout()
    fig.savefig(FIG / "intracule_comparison.png", dpi=200)
    fig.savefig(FIG / "fig1_P_u_singlet_triplet.png", dpi=200)
    plt.close(fig)

    mask = u <= 2.0
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.plot(u[mask], i_s[mask], color="#b00020", lw=2.0, label=r"singlet $i_\Gamma$")
    ax.plot(u[mask], i_t[mask], color="#1f4e79", lw=2.0, label=r"triplet $i_\Gamma$")
    ax.plot(u[mask], i_ws[mask], color="#b00020", lw=1.2, ls="--", label=r"singlet $i_{\gamma\wedge\gamma}$")
    ax.plot(u[mask], i_wt[mask], color="#1f4e79", lw=1.2, ls="--", label=r"triplet $i_{\gamma\wedge\gamma}$")
    ax.set_xlim(0, 2)
    ax.set_xlabel(r"$u=r_{12}$ (bohr)")
    ax.set_ylabel(r"$i(u)$ (bohr$^{-3}$)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Coalescence: Coulomb hole and Fermi hole")
    fig.tight_layout()
    fig.savefig(FIG / "intracule_contact.png", dpi=200)
    fig.savefig(FIG / "fig2_i_u_contact.png", dpi=200)
    plt.close(fig)

    ns = np.load(DATA / "he_singlet_natural_occupations.npy")
    nt = np.load(DATA / "he_triplet_natural_occupations.npy")
    k = min(6, ns.size, nt.size)
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    x = np.arange(k)
    ax.bar(x - 0.18, ns[:k], width=0.36, color="#b00020", label="singlet")
    ax.bar(x + 0.18, nt[:k], width=0.36, color="#1f4e79", label="triplet")
    ax.axhline(2.0, color="0.5", lw=0.7, ls=":")
    ax.axhline(1.0, color="0.5", lw=0.7, ls=":")
    ax.set_xlabel("natural orbital index")
    ax.set_ylabel("occupation")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Helium FCI natural occupations, aug-cc-pVQZ")
    fig.tight_layout()
    fig.savefig(FIG / "occupation_numbers.png", dpi=200)
    plt.close(fig)

    conv = CERT["mean_r12_vs_basis"]
    xs = np.arange(len(conv["labels"]))
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.plot(xs, conv["singlet_gamma"], "o-", color="#b00020", label=r"singlet $\Gamma$")
    ax.plot(xs, conv["triplet_gamma"], "s-", color="#1f4e79", label=r"triplet $\Gamma$")
    ax.plot(xs, conv["singlet_wedge"], "o--", color="#b00020", alpha=0.7, label="singlet wedge")
    ax.plot(xs, conv["triplet_wedge"], "s--", color="#1f4e79", alpha=0.7, label="triplet wedge")
    ax.set_xticks(xs, conv["labels"])
    ax.set_ylabel(r"$\langle r_{12}\rangle$ (bohr)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title(r"Helium mean $r_{12}$ vs basis")
    fig.tight_layout()
    fig.savefig(FIG / "r12_convergence.png", dpi=200)
    fig.savefig(FIG / "fig3_mean_r12_vs_basis.png", dpi=200)
    plt.close(fig)
    print("Wrote", FIG / "intracule_comparison.png")
    print("Wrote", FIG / "fig1_P_u_singlet_triplet.png")
    print("Wrote", FIG / "occupation_numbers.png")
    print("Wrote", FIG / "r12_convergence.png")


if __name__ == "__main__":
    main()
