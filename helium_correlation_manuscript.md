# Reproducible Reduced-Density-Matrix Descriptors for Helium Singlet and Triplet States

**Abstract**  
We present a reproducible full configuration interaction (FCI) workflow for
reduced-density-matrix analysis of the helium \(1\,^1S\) ground state and
\(2\,^3S\) excited triplet state in the aug-cc-pVQZ basis. The accompanying
open package contains spin-summed one-particle reduced density matrix
(1-RDM) natural occupations, leading two-particle reduced density matrix
(2-RDM) geminal quantities, intracule curves, analysis scripts, and
validation tests.

For the state-specific natural-occupation diagnostic, the first occupation
beyond the Hartree–Fock filling is resolved relative to the aug-cc-pVTZ/QZ
residual for both states. The leading-geminal intracule gives mean
interelectronic separations of \(1.424\) bohr for the singlet and
\(4.090\) bohr for the triplet, while the same-spin triplet contact value is
numerically negligible, as expected from the Fermi hole. Comparison with the
antisymmetrized 1-RDM product gives mean-distance cumulant corrections of
\(-0.056\) bohr and \(-0.015\) bohr for the singlet and triplet,
respectively, under the stated sign convention.

These results are presented as a reproducible finite-basis FCI realization
of established helium pair-correlation behavior. They are not intended as a
new mechanism for singlet–triplet structure or as a replacement for
high-precision Hylleraas and Pekeris-class helium benchmarks.

---

## 1. Introduction

Electron correlation is central to quantum chemistry and condensed-matter
physics, but the practical separation of exchange (Fermi) effects from
dynamical Coulomb correlation is often treated qualitatively. Helium provides
a compact test case: it contains only two electrons, admits highly accurate
full configuration interaction solutions in finite bases, and has a long
history in pair-density and intracule analysis.

The purpose of this note is not to propose a new interaction mechanism.
Rather, it documents an open, checked FCI implementation of known helium
pair-structure features using three complementary reduced-density-matrix
diagnostics:

1. **1-RDM natural occupation numbers**, using the first occupation beyond
   the Hartree–Fock filling, \(n_{\mathrm{disc}}\), compared with a
   documented TZ/QZ residual \(\varepsilon\);
2. **2-RDM leading-geminal intracules**, using \(\langle r_{12}\rangle\),
   contact behavior, and the pair-distance distribution \(P(u)\);
3. **Pair cumulants**, \(\Delta = \Gamma - \gamma\wedge\gamma\), to compare
   the correlated pair distribution with the antisymmetrized one-particle
   reference.

The comparison is between two different electronic states, \(1s^2\,^1S\) and
\(1s2s\,^3S\). Both spin symmetry and orbital occupancy change. The
exchange-containing antisymmetrized 1-RDM reference already reproduces most
of the difference in the reported mean-distance descriptor between the two
states; the residual cumulant correction is smaller on that observable.
This does not claim that the Coulomb energy, or the full physical
singlet–triplet difference, is explained by exchange alone.

---

## 2. Methods

### 2.1 FCI calculations

The calculations used the full configuration interaction implementation in
PySCF.

- **Software**: PySCF v2.14.0
- **Basis**: aug-cc-pVQZ; remainder from the same aug-cc-pVTZ / aug-cc-pVQZ
  sequence
- **States**: helium \(1\,^1S\) singlet and \(2\,^3S\) triplet
- **Validation**: six consistency checks covering trace, positivity, and
  rank properties of the reduced density matrices

The aug-cc-pVQZ basis is the augmented correlation-consistent polarized
valence quadruple-zeta basis of the Dunning family. The present FCI numbers
are a reproducible finite-basis realization, not a complete-basis or
Hylleraas-class helium benchmark.

### 2.2 1-RDM and natural orbitals

The spin-summed one-particle reduced density matrix is diagonalized as

\[
\gamma(\mathbf r,\mathbf r')
=
\sum_i n_i
\phi_i(\mathbf r)
\phi_i^*(\mathbf r'),
\]

with occupations sorted descending. The diagnostic \(n_{\mathrm{disc}}\) is
the first occupation after the Hartree–Fock filled count: singlet \(n[1]\),
triplet \(n[2]\). The residual is

\[
\varepsilon = 2\bigl|n_{\mathrm{disc}}^{\mathrm{QZ}}
- n_{\mathrm{disc}}^{\mathrm{TZ}}\bigr|
+ \delta_{\mathrm{alg}}.
\]

The inequality \(n_{\mathrm{disc}} > 2\varepsilon\) is a computational
resolution and documentation check for this finite-basis series. It is not a
new physical observable.

### 2.3 2-RDM and leading geminal

The two-particle reduced density matrix is diagonalized as

\[
\Gamma(\mathbf r_1,\mathbf r_2;
\mathbf r_1',\mathbf r_2')
=
\sum_k \lambda_k
\Phi_k(\mathbf r_1,\mathbf r_2)
\Phi_k^*(\mathbf r_1',\mathbf r_2').
\]

The pair matrix is formed as
\(G[(p,r),(q,s)] = \mathrm{transpose}(\mathrm{dm2},(0,2,1,3))\) and then
symmetrized. A naive `reshape` without that transpose is the wrong map.

The leading geminal is projected onto an intracule,

\[
I(r_{12})
=
\int
|\Phi_{\max}(\mathbf r_1,\mathbf r_2)|^2
\delta\!\left(
|\mathbf r_1-\mathbf r_2|-r_{12}
\right)
\,d\mathbf r_1\,d\mathbf r_2.
\]

Contact values \(i(0)\) and radial pair distributions \(P(u)\) are reported
from the same quadrature.

### 2.4 Pair cumulant analysis

The two-particle cumulant is

\[
\Delta = \Gamma - \gamma\wedge\gamma,
\]

where \(\gamma\wedge\gamma\) is the antisymmetrized product of the 1-RDM.
This reference includes fermionic exchange but not the remaining
two-particle correlation encoded in \(\Gamma\). For each state,

\[
\delta_c
=
\langle r_{12}\rangle_{\gamma\wedge\gamma}
-
\langle r_{12}\rangle_{\Gamma}.
\]

A negative \(\delta_c\) means that the correlated 2-RDM has a larger mean
pair separation than the antisymmetrized 1-RDM reference, for this
descriptor and sign convention.

---

## 3. Results

### 3.1 1-RDM resolution check

| State | \(n_{\max}\) | \(n_{\mathrm{disc}}\) | \(\varepsilon\) | \(n_{\mathrm{disc}}/(2\varepsilon)\) |
|---|---:|---:|---:|---:|
| Singlet | 1.98389 | 0.007609 | \(3.32\times10^{-4}\) | 11.47 |
| Triplet | 0.99962 | 0.000125 | \(2.16\times10^{-5}\) | 2.89 |

Both states satisfy \(n_{\mathrm{disc}} > 2\varepsilon\) in this
aug-cc-pVTZ/QZ remainder. The ratios are documentation of that residual
test, not a physical correlation-strength ranking independent of the
chosen \(\varepsilon\).

### 3.2 Intracule: pair separation and Fermi hole

| State | \(\langle r_{12}\rangle_\Gamma\) (bohr) | \(i(0)\) (bohr\(^{-3}\)) | \(P(u)\) peak (bohr) |
|---|---:|---:|---:|
| Singlet, \(\Gamma\) | 1.424 | 0.1245 | \(\approx 1.0\) |
| Triplet, \(\Gamma\) | 4.090 | \(\approx 0\) (\(9.7\times10^{-34}\)) | \(\approx 3.5\) |

Figure 1 (`figures/fig1_P_u_singlet_triplet.png`; also
`intracule_comparison.png`) shows \(P(u)\). Figure 2
(`figures/fig2_i_u_contact.png`; also `intracule_contact.png`) shows the
coalescence region.

The singlet leading-geminal pair is more compact than the triplet pair.
The triplet contact value is numerically negligible, as required by
same-spin spatial antisymmetry (the Fermi hole). These are established
helium pair-structure features; the present numbers are the FCI/aug-cc-pVQZ
realization in this package.

### 3.3 Pair cumulant: correction to the wedge reference

| State | \(\langle r_{12}\rangle_\Gamma\) (bohr) | \(\langle r_{12}\rangle_{\gamma\wedge\gamma}\) (bohr) | \(\delta_c\) (bohr) |
|---|---:|---:|---:|
| Singlet | 1.424 | 1.368 | \(-0.056\) |
| Triplet | 4.090 | 4.075 | \(-0.015\) |

For both states, \(\delta_c < 0\). On this mean-distance measure, the full
correlated 2-RDM is slightly more spatially separated than the
antisymmetrized 1-RDM reference. That is a cumulant-based FCI confirmation
that correlation increases the chosen mean pair distance relative to
\(\gamma\wedge\gamma\), consistent in sign with the classical observation
that correlation increases mean interelectronic separation relative to an
uncorrelated reference.

Most of the reported singlet–triplet mean-distance difference is already
present in the wedge: \(1.368\) bohr versus \(4.075\) bohr. The additional
cumulant corrections are smaller on this observable. Because the states
differ in both spin and orbital occupancy (\(1s^2\) versus \(1s2s\)), this
is not a claim that exchange accounts for the entire physical difference
between the states.

Figure 3 (`figures/fig3_mean_r12_vs_basis.png`; also
`r12_convergence.png`) shows the DZ/TZ/QZ remainder of the same
augmented sequence.

### 3.4 Comparison with high-accuracy reference values

aug-cc-pVQZ FCI is not a helium-atom accuracy benchmark against Hylleraas
or Pekeris-class wave functions.

| Quantity | This work: FCI/aug-cc-pVQZ | High-accuracy reference | Difference |
|---|---:|---:|---:|
| \(\langle r_{12}\rangle\), \(1\,^1S\) | 1.4238 bohr | approximately 1.422 bohr | approximately 0.002 bohr |
| \(\langle r_{12}\rangle\), \(2\,^3S\) | 4.0900 bohr | not entered | — |

The singlet reference is a rounded Pekeris/Hylleraas-class literature value;
the exact digit string depends on the chosen high-accuracy source and on
whether \(\langle r_{12}\rangle\) is taken from the full pair density or
from a leading-geminal projection. The triplet high-accuracy entry is left
blank until the corresponding number is read from the original tables of
Yu, Zhou and Qiao (2022), or from another primary source with the same
definition.

---

## 4. Discussion

### 4.1 What is being compared

Two statements are easy to conflate and are kept separate here.

First, the triplet’s vanishing coalescence probability follows from
same-spin exchange antisymmetry. The numerical \(i(0)\approx 0\) is the
Fermi hole appearing in this FCI intracule.

Second, \(\delta_c\) measures the change from the antisymmetrized 1-RDM
reference to the full correlated 2-RDM. For the reported mean-distance
descriptor the correction is negative. That does not imply that Coulomb
repulsion is absent from the singlet–triplet contrast, and it does not
establish a universal rule for all correlation descriptors.

### 4.2 Relation to established pair structure

Coulson and Neilson analysed the helium ground-state intracule and showed
that correlation reduces the probability of small \(r_{12}\) and increases
the mean electronic separation. Boyd and Coulson treated Coulomb and Fermi
holes in helium excited states, including \(2\,^3S\). Regier and Thakkar
and later workers reported correlated intracules for low-lying helium-like
states. Besley and Gill computed excited-state intracules, including
singlet–triplet exchange differences. Piris, López and Ugalde defined
Coulomb and Fermi holes from the 2-RDM cumulant without a Hartree–Fock
reference. Natural orbitals of two-electron systems go back to Löwdin and
Shull; high-accuracy helium occupations have been given by Davidson and by
later natural-amplitude benchmarks.

The present package is an open FCI/aug-cc-pVQZ implementation of that
picture, with explicit 1-RDM, leading-geminal, and \(\gamma\wedge\gamma\)
descriptors in one workflow.

### 4.3 Limitations

- The numbers concern helium in aug-cc-pVQZ and the observables defined
  above.
- The \(n_{\mathrm{disc}}\) residual test is a finite-basis documentation
  check, not a proof of complete-basis-set convergence.
- The leading-geminal intracule is a compact descriptor and does not
  contain every feature of the full two-electron pair density.
- The two states differ in orbital structure as well as spin.
- Full AO-basis 1-RDM and 2-RDM tensors are not part of the current
  archive.

---

## 5. Conclusion

This note provides a reproducible FCI workflow and open dataset for
reduced-density-matrix descriptors of helium \(1\,^1S\) and \(2\,^3S\) in
aug-cc-pVQZ.

Within that finite-basis realization:

- both states pass the documented \(n_{\mathrm{disc}} > 2\varepsilon\)
  residual check, with margins 11.47 (singlet, index 1) and 2.89
  (triplet, index 2);
- the leading-geminal mean pair distances are \(1.424\) bohr and
  \(4.090\) bohr;
- the triplet contact value is numerically a Fermi hole;
- relative to \(\gamma\wedge\gamma\), the correlated 2-RDM increases the
  mean pair separation by \(0.056\) bohr (singlet) and \(0.015\) bohr
  (triplet) under the stated sign convention.

The value of the work is the transparent implementation, the frozen
definitions, and the reusable analysis pipeline. It is not a new account of
helium pair physics.

---

## Data and Code Availability

The source repository is

https://github.com/kaiplaketti/helium-correlation-data

The reserved Zenodo version DOI is `10.5281/zenodo.22837641`. That
identifier is a draft reservation and returns 404 until the deposition is
published from a tagged snapshot; the 404 is expected and the identifier
must not be replaced.

The archive contains certified summary quantities, natural-occupation data,
leading-geminal quantities, intracule curves, analysis scripts, figures, and
documentation. Full AO-basis 1-RDM and 2-RDM tensors are not included in the
current release.

Code in `scripts/` is MIT-licensed. Data, figures, and documentation follow
the repository data license.

---

## Acknowledgements

We thank our family for their support and patience during this work.

---

## References

1. Coulson, C. A., & Neilson, A. H. (1961). Electron Correlation in the Ground
   State of Helium. *Proceedings of the Physical Society*, **78**(5), 831–837.
   https://doi.org/10.1088/0370-1328/78/5/328

2. Löwdin, P.-O., & Shull, H. (1956). Natural Orbitals in the Quantum Theory
   of Two-Electron Systems. *Physical Review*, **101**, 1730–1739.
   https://doi.org/10.1103/PhysRev.101.1730

3. Coleman, A. J. (1963). Structure of Fermion Density Matrices.
   *Reviews of Modern Physics*, **35**, 668–686.
   https://doi.org/10.1103/RevModPhys.35.668

4. Davidson, E. R. (1963). Natural Expansions of Exact Wave Functions. III.
   The Helium-Atom Ground State. *The Journal of Chemical Physics*, **39**,
   875–880. https://doi.org/10.1063/1.1734386

5. Boyd, R. J., & Coulson, C. A. (1973). Coulomb hole in some excited states
   of helium. *Journal of Physics B: Atomic and Molecular Physics*, **6**,
   782–793. https://doi.org/10.1088/0022-3700/6/5/012

6. Boyd, R. J., & Coulson, C. A. (1974). The Fermi hole in atoms.
   *Journal of Physics B: Atomic and Molecular Physics*, **7**, 1805–1816.
   https://doi.org/10.1088/0022-3700/7/14/006

7. Pekeris, C. L. (1959). \(1^1S\) and \(2^3S\) States of Helium.
   *Physical Review*, **115**, 1216–1221.
   https://doi.org/10.1103/PhysRev.115.1216

8. Thakkar, A. J., & Smith, V. H. (1977). Accurate charge densities and
   two-electron intracule functions for the heliumlike ions.
   *The Journal of Chemical Physics*, **67**, 1191–1196.
   https://doi.org/10.1063/1.434974

9. Regier, P. E., & Thakkar, A. J. (1984). Charge densities and two-electron
   intracules for the low-lying excited states of the helium-like ions.
   *Journal of Physics B: Atomic and Molecular Physics*, **17**, 3391–3403.
   https://doi.org/10.1088/0022-3700/17/17/011

10. Besley, N. A., & Gill, P. M. W. (2004). Atomic and molecular intracules
    for excited states. *The Journal of Chemical Physics*, **120**, 7290–7297.
    https://doi.org/10.1063/1.1690233

11. Piris, M., López, X., & Ugalde, J. M. (2008). Correlation holes for the
    helium dimer. *The Journal of Chemical Physics*, **128**, 134102.
    https://doi.org/10.1063/1.2883959

12. Cioslowski, J., & Prątnicki, F. (2019). Natural amplitudes of the ground
    state of the helium atom: Benchmark calculations and their relevance to
    the issue of unoccupied natural orbitals in the H\(_2\) molecule.
    *The Journal of Chemical Physics*, **150**, 074111.
    https://doi.org/10.1063/1.5065791

13. Cioslowski, J., & Strasburger, K. (2025). Reconstruction of the On-Top
    Two-Electron Density from Natural Orbitals and Their Occupation Numbers.
    *Journal of Chemical Theory and Computation*, **21**, 3945–3952.
    https://doi.org/10.1021/acs.jctc.5c00024

14. Yu, Y., Zhou, C., & Qiao, H. (2022). Geometric structure parameters of
    ground and singly excited states of helium. *The European Physical
    Journal D*, **76**, 26.
    https://doi.org/10.1140/epjd/s10053-021-00317-y

15. Sun, Q., et al. (2020). Recent developments in the PySCF program package.
    *The Journal of Chemical Physics*, **153**, 024109.
    https://doi.org/10.1063/5.0006074

16. Kendall, R. A., Dunning, T. H., Jr., & Harrison, R. J. (1992). Electron
    affinities of the first-row atoms revisited: Systematic basis sets and
    wave functions. *The Journal of Chemical Physics*, **96**, 6796–6806.
    https://doi.org/10.1063/1.462569

17. Helgaker, T., Jørgensen, P., & Olsen, J. (2000).
    *Molecular Electronic-Structure Theory*. Wiley.
