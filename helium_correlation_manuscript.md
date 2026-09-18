# Certified Electron Correlation in Helium: Exchange Dominates, Coulomb Loosens

**Abstract**  
We present a quantitative certification of two-electron correlation in helium
using full configuration interaction (FCI) calculations in the aug-cc-pVQZ
basis. Natural orbitals from the one-particle reduced density matrix (1-RDM)
show a clear difference in non-idempotency between the singlet and triplet
states. The leading two-particle reduced density matrix (2-RDM) geminal
intracule shows that the opposite-spin singlet pair is on average closer
together, with \(\langle r_{12}\rangle = 1.424\) bohr, than the same-spin
triplet pair, with \(\langle r_{12}\rangle = 4.090\) bohr. The triplet
intracule vanishes at coalescence, consistent with the Fermi hole. Pair
cumulant analysis,
\(\Delta = \Gamma - \gamma\wedge\gamma\), further shows that Coulomb
correlation increases the singlet pair separation by
\(\delta_c = -0.056\) bohr relative to the antisymmetrized 1-RDM reference.
The underlying FCI data, analysis scripts, and figures are available in
reproducible archived form.

---

## 1. Introduction

Electron correlation is central to quantum chemistry and condensed-matter
physics, but the practical separation of exchange (Fermi) effects from
dynamical Coulomb correlation is often treated qualitatively. Helium provides
a compact test case: it contains only two electrons, admits highly accurate
full configuration interaction solutions in finite bases, and has a long
history in pair-density and intracule analysis.

Here, helium correlation is assessed with three complementary diagnostics:

1. **1-RDM natural occupation numbers**, using non-idempotency measured by
   \(n_{\mathrm{disc}}\) relative to a basis-set residual \(\varepsilon\);
2. **2-RDM leading-geminal intracules**, using
   \(\langle r_{12}\rangle\), contact behavior, and the position of the
   pair-distance distribution;
3. **Pair cumulants**,
   \(\Delta = \Gamma - \gamma\wedge\gamma\), to compare the correlated
   pair distribution with the antisymmetrized one-particle reference.

The purpose is not to propose a new interaction mechanism. Rather, this work
provides a transparent and reproducible numerical decomposition of pair
structure in a canonical two-electron system.

---

## 2. Methods

### 2.1 FCI calculations

The calculations were performed using the full configuration interaction
implementation in PySCF.

- **Software**: PySCF v2.14.0
- **Basis**: aug-cc-pVQZ
- **States**: helium \(1\,^1S\) singlet and \(2\,^3S\) triplet
- **Validation**: six consistency checks covering trace, positivity, and rank
  properties of the reduced density matrices

The aug-cc-pVQZ basis is the augmented correlation-consistent polarized
valence quadruple-zeta basis of the Dunning family. The diffuse augmentation
is relevant for accurate spatial pair distributions and for the excited
triplet state.

### 2.2 1-RDM and natural orbitals

The one-particle reduced density matrix is diagonalized as

\[
\gamma(\mathbf r,\mathbf r')
=
\sum_i n_i
\phi_i(\mathbf r)
\phi_i^*(\mathbf r').
\]

For an uncorrelated closed-shell determinant, the spatial natural occupations
are idempotent in the appropriate spin-summed representation. Departures from
this limiting occupation pattern provide a compact correlation diagnostic.

We use \(n_{\mathrm{disc}}\) to denote the reported non-idempotent occupation
weight and compare it with twice the estimated TZ/QZ residual,
\(2\varepsilon\). A value satisfying

\[
n_{\mathrm{disc}} > 2\varepsilon
\]

is treated as resolved with respect to this residual estimate.

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

The leading geminal is projected onto an intracule distribution,

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

The intracule characterizes the distribution of electron-pair separations.
Its behavior near \(r_{12}=0\) directly distinguishes the opposite-spin
singlet pair from the same-spin triplet pair.

### 2.4 Pair cumulant analysis

The two-particle cumulant is defined by

\[
\Delta
=
\Gamma-\gamma\wedge\gamma,
\]

where \(\gamma\wedge\gamma\) is the antisymmetrized product of the 1-RDM.
This reference includes the exchange structure associated with fermionic
antisymmetry but does not contain the full two-particle correlation encoded
in \(\Gamma\).

For each state, we define

\[
\delta_c
=
\langle r_{12}\rangle_{\gamma\wedge\gamma}
-
\langle r_{12}\rangle_{\Gamma}.
\]

With this sign convention, a negative \(\delta_c\) means that the correlated
2-RDM has a larger mean pair separation than the antisymmetrized 1-RDM
reference.

---

## 3. Results

### 3.1 1-RDM: correlation diagnostic

| State | \(n_{\max}\) | \(n_{\mathrm{disc}}\) | \(\varepsilon\) | \(n_{\mathrm{disc}} > 2\varepsilon\)? |
|---|---:|---:|---:|---|
| Singlet | 1.98389 | 0.007609 | \(3.32\times10^{-4}\) | **PASS**; approximately \(11.5\times\) the threshold |
| Triplet | 0.99962 | 0.000125 | \(2.16\times10^{-5}\) | **PASS**; approximately \(2.9\times\) the threshold |

Both states pass the chosen resolution criterion. The singlet displays a
substantially larger reported non-idempotent occupation weight than the
triplet, consistent with a stronger dynamical-correlation signature in the
singlet 1-RDM.

### 3.2 Intracule: coalescence and pair separation

| State | \(\langle r_{12}\rangle\) (bohr) | \(i(0)\) | \(P(u)\) peak (bohr) |
|---|---:|---:|---:|
| Singlet, \(\Gamma\) | 1.424 | 0.1245 | approximately 1.0 |
| Triplet, \(\Gamma\) | 4.090 | approximately 0 | approximately 3.5 |

The singlet pair is considerably more compact than the triplet pair. At
coalescence, the same-spin triplet pair has vanishing contact probability,
as required by antisymmetry of the spatial wavefunction. This is the
familiar Fermi hole.

The large singlet–triplet difference in \(\langle r_{12}\rangle\) should be
interpreted in conjunction with the distinct electronic states and orbital
structure of \(1\,^1S\) and \(2\,^3S\), rather than as a Coulomb-only effect.

### 3.3 Pair cumulant: Coulomb correction to the wedge reference

| State | \(\langle r_{12}\rangle_\Gamma\) (bohr) | \(\langle r_{12}\rangle_{\gamma\wedge\gamma}\) (bohr) | \(\delta_c\) (bohr) |
|---|---:|---:|---:|
| Singlet | 1.424 | 1.368 | \(-0.056\) |
| Triplet | 4.090 | 4.075 | \(-0.015\) |

For both states, \(\delta_c < 0\). Under the convention used here, the full
correlated 2-RDM has a slightly larger mean pair separation than the
antisymmetrized 1-RDM reference. Thus, for this specific mean-distance
descriptor, the Coulomb contribution shifts the pair outward relative to the
exchange-containing wedge reference.

The singlet–triplet separation difference is already largely present in the
antisymmetrized 1-RDM reference:
\(1.368\) bohr for the singlet versus \(4.075\) bohr for the triplet. The
additional cumulant correction is comparatively small on this metric.

---

## 4. Discussion

### 4.1 Exchange and Coulomb contributions

The results distinguish two different statements that are sometimes
conflated.

First, the triplet’s vanishing coalescence probability follows from
same-spin exchange antisymmetry. The Fermi hole is therefore an exchange
effect.

Second, the pair cumulant measures the change from the antisymmetrized 1-RDM
reference to the full correlated 2-RDM. On the mean-distance measure used
here, this correction is negative:

\[
\delta_c < 0.
\]

Accordingly, the full Coulomb-correlated pair is slightly more spatially
separated than the wedge reference. This does not imply that Coulomb
repulsion is absent from the singlet–triplet contrast, nor does it establish
a universal rule for all correlation descriptors. It states a precise,
reproducible result for the reported FCI data and the chosen observable.

### 4.2 Relation to established pair structure

The compact singlet pair and the triplet Fermi hole are consistent with the
standard physical picture of helium pair structure. The present calculations
make those features directly measurable through natural occupations,
leading-geminal intracules, and a cumulant-derived comparison to the
antisymmetrized 1-RDM reference.

The use of a common analysis workflow for both states makes the numerical
comparison explicit and reproducible.

### 4.3 Limitations

This study has several limitations.

- The conclusions concern helium in the aug-cc-pVQZ basis and the particular
  observables reported here.
- The 1-RDM residual comparison is a finite-basis diagnostic, not a proof of
  complete-basis-set convergence.
- The leading-geminal intracule is a compact descriptor and does not contain
  every feature of the full two-electron pair density.
- The reported comparison concerns two different electronic states,
  \(1\,^1S\) and \(2\,^3S\), whose orbital structures differ in addition to
  their spin symmetry.
- Extension to three-electron systems, such as lithium, will introduce
  additional representability, state-selection, and computational issues.

---

## 5. Conclusion and Outlook

We have provided a reproducible FCI-based analysis of electron-pair
correlation in helium using three complementary reduced-density-matrix
diagnostics.

The principal quantitative findings are:

- the singlet has a substantially larger non-idempotent occupation signature
  than the triplet;
- the singlet leading-geminal pair is more compact than the triplet pair;
- the triplet contact probability vanishes, revealing the Fermi hole;
- relative to the antisymmetrized 1-RDM reference, the full correlated 2-RDM
  increases the mean pair separation by \(0.056\) bohr for the singlet and
  \(0.015\) bohr for the triplet under the stated sign convention.

The dataset and analysis scripts provide a reference implementation for
extending the same workflow to larger few-electron systems, including
lithium.

---

## Data and Code Availability

The complete FCI data, analysis scripts, figures, and documentation
supporting this work are archived on Zenodo at:

https://doi.org/10.5281/zenodo.22837641

The corresponding source repository is available at:

https://github.com/kaiplaketti/helium-correlation-data

---

## Acknowledgements

We thank our family for their support and patience during this work.

---

## References

1. Coulson, C. A., & Neilson, A. H. (1961). Electron correlation in helium
   and related intracule analyses. *Proceedings of the Physical Society*,
   **78**, 831.

2. Shull, H., & Löwdin, P.-O. (1956). Correlation in the helium atom and
   reduced-density-matrix analysis. *Physical Review*, **101**, 1730.

3. Coleman, A. J. (1963). Structure of fermion density matrices.
   *Reviews of Modern Physics*, **35**, 668.

4. Sun, Q., Berkelbach, T. C., Blunt, N. S., Booth, G. H., Guo, S.,
   Li, Z., Liu, J., McClain, J. D., Sayfutyarova, E. R., Sharma, S.,
   Wouters, S., & Chan, G. K.-L. (2020). PySCF: The Python-based
   simulations of chemistry framework. *Journal of Chemical Physics*,
   **153**, 024109. https://doi.org/10.1063/5.0006074

5. Helgaker, T., Jørgensen, P., & Olsen, J. (2000).
   *Molecular Electronic-Structure Theory*. Wiley.

6. Kendall, R. A., Dunning, T. H., Jr., & Harrison, R. J. (1992).
   Electron affinities of the first-row atoms revisited: Systematic basis
   sets and wave functions. *Journal of Chemical Physics*, **96**,
   6796–6806. https://doi.org/10.1063/1.462569
