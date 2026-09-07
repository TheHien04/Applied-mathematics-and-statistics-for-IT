# Applied Mathematics and Statistics for Information Technology

| Field | Record |
|:------|:-------|
| **Course** | MTH00051 — Applied Mathematics and Statistics |
| **Institution** | Faculty of Information Technology, University of Science, VNU–HCM |
| **Author** | Nguyễn Thế Hiển · Student ID `22127107` · Class `22CLC08` |
| **Period** | Academic years 2024–2026 |
| **Corpus** | Seven laboratory projects and two capstone dissertations |
| **MSC 2020** | 15A06, 15A18, 15A23, 62J05, 62H30, 60J10, 68U10 |
| **Primary objects** | $Ax=b$, $A=QR$, $A=PDP^{-1}$, OLS, finite Markov kernels |

---

## Abstract

This repository is a complete, reproducible archive of the MTH00051 curriculum. Each artefact pairs a classical construction in linear algebra or statistical modelling with a from-scratch Python realisation and, where the assignment requires it, a formal academic report. The laboratory sequence treats unsupervised colour quantisation in $\mathbb{R}^3$, discrete image operators (pointwise maps, geometry, 2-D convolution), and ordinary least squares with $K$-fold model selection. The computational-algebra block implements Gaussian elimination with partial pivoting, classical Gram–Schmidt $QR$, spectral factorisation $A=PDP^{-1}$ via the characteristic polynomial and Gauss–Jordan inversion, and multivariate OLS on physicochemical wine data. Two dissertations close the course: a three-state Markov model of S&P 500 log-return regimes, and a hedonic-pricing study of Stockton residential sales together with a finite traffic chain.

Library factorisations (`numpy.linalg.solve`, `numpy.linalg.qr`, `numpy.linalg.eig`) are used exclusively as independent numerical witnesses. Student solvers follow defining equations, report ranks and residual norms, and record seeds, fold protocols, and state thresholds so that every table in the reports can be regenerated.

**Keywords.** Gaussian elimination; Gram–Schmidt; matrix diagonalization; ordinary least squares; $k$-means; discrete convolution; Markov chains; cross-validation; hedonic pricing; computational linear algebra.

---

## Contents

1. [Abstract](#abstract)
2. [Positioning and contributions](#positioning-and-contributions)
3. [Notation](#notation)
4. [Computational contract](#computational-contract)
5. [Mathematical scope](#mathematical-scope)
6. [Principal findings](#principal-findings)
7. [Repository structure](#repository-structure)
8. [Data provenance](#data-provenance)
9. [Project 1 — Colour compression via $k$-means](#project-1--colour-compression-via-k-means)
10. [Project 2 — Image processing](#project-2--image-processing)
11. [Project 3 — Linear regression](#project-3--linear-regression)
12. [Project 4 — Gaussian elimination](#project-4--gaussian-elimination)
13. [Project 5 — Gram–Schmidt $QR$](#project-5--gramschmidt-qr)
14. [Project 6 — Diagonalizable matrices](#project-6--diagonalizable-matrices)
15. [Project 7 — Wine-quality OLS](#project-7--wine-quality-ols)
16. [Final 1 — Markov regimes on the S&P 500](#final-1--markov-regimes-on-the-sp-500)
17. [Final 2 — Stockton prices and a traffic chain](#final-2--stockton-prices-and-a-traffic-chain)
18. [Limitations](#limitations)
19. [Environment and reproduction](#environment-and-reproduction)
20. [Report convention](#report-convention)
21. [Academic integrity](#academic-integrity)
22. [How to cite](#how-to-cite)
23. [Instructors](#instructors)
24. [References](#references)

---

## Positioning and contributions

The archive is not a collection of tutorial notebooks. It is a sequence of *constructive* arguments: each algorithm is stated, implemented from the statement, tested against an independent library, and discussed with its hypotheses and failure modes. Three claims organise the work.

1. **Linear systems are the computational backbone.** Gaussian elimination, $QR$, and $PDP^{-1}$ are developed as explicit maps, then reused to solve normal equations and to evolve Markov kernels.
2. **Statistical models are identified by a declared risk.** Projects 3 and 7 and Final 2 report MAE, MSE/$R^2$, or $\lVert e\rVert_2$ under a protocol that forbids leakage (single shuffle, in-fold standardisation, dollar-scale scoring of log-linear fits).
3. **Stochastic kernels are estimated, powered, and diagnosed.** Final 1 and Final 2 construct $\hat P$ by counts, compute $P^t$ by exponentiation, and solve $\pi P=\pi$ as a linear system, with a second-order memory check where data permit.

Pedagogically the corpus splits into three blocks.

| Block | Folders | Role in the curriculum |
|:------|:--------|:-----------------------|
| Laboratory sequence | Projects 1–3 | Geometry of clustering, discrete image operators, OLS with a held-out test set |
| Computational linear algebra | Projects 4–7 | Existence for $Ax=b$, orthonormal factors, spectral powers, multivariate OLS |
| Capstone dissertations | Final 1, Final 2 | Markov regimes on equity returns; hedonic pricing and a finite traffic chain |

---

## Notation

| Symbol | Meaning |
|:-------|:--------|
| $A\in\mathbb{R}^{m\times n}$ | Data or coefficient matrix; columns $a_1,\ldots,a_n$ |
| $[A\mid b]$ | Augmented matrix of $Ax=b$ |
| $Q,R$ | Thin $QR$ factors; $Q^\top Q=I_n$, $R$ upper triangular |
| $P,D$ | Eigenvector matrix and diagonal matrix of eigenvalues |
| $X,y$ | Design matrix (typically intercept-augmented) and response |
| $\hat w,\hat\beta,\hat\theta$ | OLS coefficients; $\hat w=\arg\min_w\lVert Xw-y\rVert_2^2$ |
| $\mathrm{MAE},\mathrm{MSE},R^2$ | Mean absolute error, mean squared error, coefficient of determination |
| $\hat P=(p_{ij})$ | Row-stochastic transition kernel; $\hat p_{ij}=N_{ij}/\sum_k N_{ik}$ |
| $\pi$ | Stationary law, $\pi P=\pi$, $\sum_i\pi_i=1$, $\pi_i\ge 0$ |
| $\lVert\cdot\rVert_2,\lVert\cdot\rVert_\infty$ | Euclidean and max norms |

Throughout, “library check” means a comparison *after* the student routine has returned, never a substitution for it.

---

## Computational contract

Every student solver in this repository obeys the same discipline.

- **Defining equations first.** Centroids are sample means; convolution is a double sum; OLS solves $X^\top X\,\hat\beta=X^\top y$; $\hat P$ is a row-normalised count matrix.
- **No silent library path.** `numpy.linalg.qr` / `eig` / `solve` may confirm a residual; they do not compute the submitted factorisation.
- **Invariants are stated and measured.** $QR\approx A$, $Q^\top Q\approx I$, $PDP^{-1}\approx A$, $\pi\hat P\approx\pi$, row sums of $\hat P$ equal $1$.
- **Protocol is part of the result.** Shuffle-once cross-validation, in-fold scaling, state threshold $k$, and RNG seeds are recorded in the notebook that produced the table.
- **Comparison is on the invariant, not on a gauge.** Eigenvectors may differ by sign and scale; Householder $QR$ may differ from Gram–Schmidt in sign pattern. The test is reconstruction.

---

## Mathematical scope

| Item | Core theme | Mathematical objects | Intended outcome |
|:----:|:-----------|:---------------------|:-----------------|
| **1** | Unsupervised colour quantisation | $k$-means on RGB vectors in $\mathbb{R}^3$; empirical risk $J$ | Prototype clustering and palette compression |
| **2** | Digital image processing | Pointwise maps; geometric maps; discrete 2-D convolution | Linear-algebraic view of filtering and geometry |
| **3** | Supervised linear prediction | OLS, MAE, $5$-fold cross-validation | Model selection and honest error estimation |
| **4** | Direct solution of linear systems | Gaussian elimination with partial pivoting; back substitution | Existence, uniqueness, and a constructive $x$ for $Ax=b$ |
| **5** | Orthogonal factorisation | Classical Gram–Schmidt; $A=QR$ | Orthonormal bases and a triangular factor |
| **6** | Spectral factorisation | Characteristic polynomial; eigenpairs; $A=PDP^{-1}$ | Diagonalisation with Gauss–Jordan inversion |
| **7** | Multivariate OLS | Normal equations; $5$-fold CV; forward selection | Feature design under out-of-sample comparison |
| **F1** | Discrete-time market regimes | Stochastic kernel $\hat P$; $v_t=v_0P^t$; stationary $\pi$ | Regime classification, forecast, Markov diagnostics |
| **F2** | Hedonic prices and a traffic chain | Residual $\lVert e\rVert_2$; polynomial / interaction designs; finite kernel | In-sample ranking and Chapman–Kolmogorov evolution |

---

## Principal findings

Headline numbers are those reported in the corresponding notebook. They are not re-estimated in this README.

| Artefact | Claim | Evidence |
|:---------|:------|:---------|
| Project 3 | Full five-feature OLS dominates sparse alternatives on the test set | Test MAE $1.596$ versus $6.5443$ (best singleton) and $1.6943$ (Hours + Previous + Sleep) |
| Project 4 | Worked $3\times 3$ system has the unique solution $(5,3,-2)$ | Agrees with `numpy.linalg.solve` |
| Project 5 | Classical Gram–Schmidt reconstructs $A$ to machine precision | $\|A-QR\|_\infty\approx 7.56\times 10^{-16}$ against Householder QR |
| Project 6 | Both demonstration matrices are recovered from $PDP^{-1}$ | Residuals $0$ and $\approx 1.29\times 10^{-15}$ |
| Project 7 | Forward selection improves on the raw eleven-feature OLS | CV MSE $0.4007$ versus $0.4166$ (full) and $0.4887$ (alcohol only) |
| Final 1 | Sideway is the sticky, dominant regime; mixing by $t=20$ | $\hat p_{11}\approx 0.59$; $\pi\approx(0.217,0.537,0.246)$ |
| Final 1 | First-order Markov is an approximation | Second-order MAE $\approx 0.052$ |
| Final 2 | Quadratic / interaction hedonic design attains the smallest in-sample residual | $\lVert e\rVert_2=1{,}312{,}397$, RMSE $\$33{,}886$, $R^2=0.713$ |
| Final 2 | Traffic chain mixes by step $10$ | $\pi\approx(0.356,0.304,0.340)$ on $(\mathrm{K},\mathrm{B},\mathrm{T})$ |

---

## Repository structure

```text
.
├── README.md
├── Project 1/
│   ├── Lab1.ipynb                              # k-means colour compression
│   └── Lab1.pdf                                # Academic laboratory report
├── Project2/
│   ├── Lab2.ipynb                              # Image-processing toolbox
│   └── Lab2.pdf                                # Academic laboratory report
├── Project3/
│   ├── Lab3.ipynb                              # Linear regression experiments
│   ├── Lab3.pdf                                # Academic laboratory report
│   ├── train.csv                               # Training split (n = 9,000)
│   └── test.csv                                # Held-out test split (n = 1,000)
├── Project4/
│   └── 22127107.ipynb                          # Gaussian elimination
├── Project5/
│   ├── 22127107.ipynb                          # Gram–Schmidt QR
│   └── Toan UDTK_Project_2-Gram-Schmidt.pdf    # Assignment brief
├── Project6/
│   ├── 22127107.ipynb                          # Matrix diagonalisation
│   └── Toan UDTK_Project_3-Diagonal matrix.pdf
├── Project7/
│   ├── 22127107.ipynb                          # Wine-quality OLS
│   ├── Toan UDTK_Project_4-Linear Regression.pdf
│   └── wine.csv                                # n = 1,199 physicochemical samples
├── Final 1/
│   ├── 22127107-NguyenTheHien.ipynb            # S&P 500 Markov regimes
│   ├── 22127107-NguyenTheHien.pdf              # Dissertation
│   ├── 22127107-NguyenTheHien.csv              # Daily OHLCV (^GSPC)
│   └── Do an cuoi ky.pdf                       # Capstone brief
└── Final 2/
    ├── 22127107-nguyenthehien.ipynb            # Stockton prices + traffic chain
    ├── 22127107-nguyenthehien.pdf              # Dissertation
    ├── Do an cuoi ky.pdf
    ├── stockton4.csv                           # n = 1,500 residential sales
    └── stockton4.def                           # Variable dictionary
```

Each folder is autarkic. The notebook is the computational artefact; the PDF, when present, is the archival write-up (problem, theory, method, experiments, discussion, references). Course briefs sit beside the solutions that answer them.

Folder names follow the laboratory numbering of the course (`Project 1` … `Project7`, `Final 1`, `Final 2`). Internal titles of later notebooks (for example, “Project 3: Gram–Schmidt” inside the computational-algebra sequence) are not a second global index.

---

## Data provenance

| File | $n$ | Role | Notes |
|:-----|----:|:-----|:------|
| `Project3/train.csv` | 9,000 | Train for student-performance OLS | EDA and CV use this split only |
| `Project3/test.csv` | 1,000 | Held-out evaluation | Untouched until the selected model is frozen |
| `Project7/wine.csv` | 1,199 | Physicochemical covariates + sensory `quality` | No external test file; comparison is $5$-fold CV |
| `Final 1/22127107-NguyenTheHien.csv` | 1,912 daily bars | `^GSPC` OHLCV, 2 Jan 2019 – 11 Aug 2026 | 1,911 log-returns after the first difference |
| `Final 2/stockton4.csv` | 1,500 | Stockton sales, Oct 1996 – Nov 1998 | Knight, University of the Pacific; see `.def` |
| `Final 2/stockton4.def` | — | Codebook | Units of `livarea`, coding of `lgelot` and `pool` |

Image rasters for Projects 1–2 are loaded inside the notebooks and are not stored as standalone CSV.

---

## Project 1 — Colour compression via $k$-means

**Objective.** Represent an RGB image by a palette of $k$ colours: cluster pixels and replace each pixel by its centroid.

**Formulation.** Each pixel is a vector $x_i\in\{0,\ldots,255\}^3\subset\mathbb{R}^3$. Centroids $\mu_1,\ldots,\mu_k$ and labels $c_i\in\{1,\ldots,k\}$ minimise

$$
J=\sum_{i=1}^{n}\bigl\lVert x_i-\mu_{c_i}\bigr\rVert_2^2.
$$

Lloyd iteration alternates nearest-centroid assignment and mean update. Initialisation is random or in-pixel; convergence is declared when centroids are stationary (`numpy.allclose`).

**Implementation.** Vectorised pixel matrix; a fully written $k$-means loop; reconstructions for $k\in\{3,5,7\}$ under several initialisations; MSE and visual fidelity in the report.

**Deliverables.** `Project 1/Lab1.ipynb`, `Project 1/Lab1.pdf`

---

## Project 2 — Image processing

**Objective.** A coherent toolbox of elementary digital-image operators under the course library constraint (NumPy, Pillow, Matplotlib; no black-box filters).

**Families.**

1. **Pointwise maps** — brightness, contrast, ITU-R BT.601 luma, sepia as an affine map on RGB.
2. **Geometry** — flip, centre crop, elliptical / double-ellipse masks with angle $\alpha$, bilinear resize.
3. **Linear filtering** — same-size 2-D convolution with edge padding,

$$
(I*K)(x,y)=\sum_{i=-a}^{a}\sum_{j=-b}^{b} K(i,j)\,I(x-i,y-j),
$$

applied channel-wise for box blur and sharpening.

**Implementation.** Explicit `_convolve2d` (spatial 2-D convolution, not a 1-D pass on a flattened raster); docstrings on every required operator; interactive `main` with per-operator and apply-all modes; saved visual outputs.

**Deliverables.** `Project2/Lab2.ipynb`, `Project2/Lab2.pdf`

---

## Project 3 — Linear regression

**Objective.** Predict **Student Performance Index** from five academic and lifestyle covariates by OLS, with model selection by cross-validated MAE.

**Features.** Hours Studied, Previous Scores, Extracurricular Activities, Sleep Hours, Sample Question Papers Practiced.  
**Response.** Performance Index (continuous).  
**Sample.** `train.csv` ($n=9000$), `test.csv` ($n=1000$).

**Formulation.**

$$
\hat y=X\hat w,\qquad
\hat w=\arg\min_w\lVert Xw-y\rVert_2^2,\qquad
\mathrm{MAE}=\frac1n\sum_{i=1}^{n}\lvert y_i-\hat y_i\rvert.
$$

Selection uses **five-fold cross-validation** after shuffling the training set **exactly once**, scoring mean validation MAE. The same permutation is reused for requirements 2b and 2c.

| Req. | Task | Selected model | Key metric |
|:----:|:-----|:---------------|:-----------|
| 1 | Exploratory analysis (train only) | — | Correlations, distributions, missingness |
| 2a | OLS on all five features | Full model | Test MAE **1.596** |
| 2b | Best singleton via 5-fold CV | Previous Scores | CV MAE **6.6182** · test MAE **6.5443** |
| 2c | Custom designs, same CV protocol | Hours + Previous + Sleep | CV MAE **1.7021** · test MAE **1.6943** |

**Implementation.** Helpers `mae`, `regression_formula`, `design_matrix`; coefficients reported to three decimals; English notebook aligned with the PDF report.

**Deliverables.** `Project3/Lab3.ipynb`, `Project3/Lab3.pdf`, `Project3/train.csv`, `Project3/test.csv`

---

## Project 4 — Gaussian elimination

**Objective.** Solve $Ax=b$ by elementary row operations. The student path does not call a black-box linear solver.

**Formulation.** Form $[A\mid b]$ and reduce to row-echelon form. At column $i$, partial pivoting selects the largest absolute entry on or below the diagonal; the pivot row is scaled to $1$ and entries below the pivot are annihilated. Back substitution recovers $x$. The algorithm distinguishes the three classical alternatives:

- unique solution if $\mathrm{rank}(A)=\mathrm{rank}([A\mid b])=n$;
- no solution if a zero row of $A$ faces a nonzero right-hand side;
- infinitely many solutions if the rank is strictly less than the number of unknowns.

**Worked example.**

$$
\begin{aligned}
x+y+z&=6,\\
2y+5z&=-4,\\
2x+5y-z&=27,
\end{aligned}
$$

returns $x=(5,3,-2)$, in agreement with `numpy.linalg.solve`.

**Implementation.** `Gauss_elimination(A)` — forward elimination with partial pivoting on a list-of-lists augmented matrix; `back_substitution(A)` — uniqueness / inconsistency / under-determination; NumPy used only as a witness.

**Deliverables.** `Project4/22127107.ipynb`

---

## Project 5 — Gram–Schmidt $QR$

**Objective.** Factor a full-column-rank matrix $A\in\mathbb{R}^{m\times n}$ as $A=QR$ by classical Gram–Schmidt, then verify orthonormality and reconstruction.

**Formulation.** With $A=[a_1,\ldots,a_n]$,

$$
u_k=a_k-\sum_{j=1}^{k-1}(q_j^\top a_k)\,q_j,
\qquad
q_k=\frac{u_k}{\lVert u_k\rVert_2},\qquad R=Q^\top A.
$$

Linear dependence is detected when $\lVert u_k\rVert_2=0$. Classical complexity is $O(mn^2)$. Sign patterns of $(Q,R)$ need not match Householder QR; the invariants are $QR=A$ and $Q^\top Q=I_n$.

**Checks.**
- Square $A\in\mathbb{R}^{3\times 3}$: $A\approx QR$ and $Q^\top Q\approx I$.
- Tall $A_2\in\mathbb{R}^{3\times 2}$: the same identities.
- Against `numpy.linalg.qr`: $\|A-QR\|_\infty\approx 7.56\times 10^{-16}$.

**Implementation.** Single routine `gram_schmidt_qr(A)` with an explicit rank-deficiency error; no library QR inside the factorisation; discussion of least squares, eigenvalue iterations, and stability relative to modified Gram–Schmidt and Householder.

**Deliverables.** `Project5/22127107.ipynb`, `Project5/Toan UDTK_Project_2-Gram-Schmidt.pdf`

---

## Project 6 — Diagonalizable matrices

**Objective.** For a diagonalizable square $A$, construct $P$, $D$, and $P^{-1}$ such that $A=PDP^{-1}$, using only course-level linear algebra.

**Formulation.**

1. Coefficients of $\det(\lambda I-A)$ by the Faddeev–LeVerrier recurrence; roots are the eigenvalues $\lambda_i$.
2. For each $\lambda_i$, a basis of $\ker(A-\lambda_i I)$ from the RREF of the homogeneous system.
3. Columns of $P$ are eigenvectors; $D=\mathrm{diag}(\lambda_1,\ldots,\lambda_n)$.
4. $P^{-1}$ by Gauss–Jordan on $[P\mid I]$. Reconstruction $\hat A=PDP^{-1}$.

A standard application is $A^k=PD^k P^{-1}$.

| Matrix | Eigenvalues (student) | $\|A-PDP^{-1}\|$ | NumPy reconstruction |
|:------:|:----------------------|:----------------:|:---------------------|
| $A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$ | $2,3$ | $0$ | $\approx 1.11\times 10^{-16}$ |
| $A_2\in\mathbb{R}^{3\times 3}$ | $1,2,3$ | $\approx 1.29\times 10^{-15}$ | consistent |

Eigenvectors may differ from `numpy.linalg.eig` by scaling and sign; the criterion is reconstruction of $A$, not entrywise equality of $P$.

**Implementation.** `rref`, `gauss_jordan_inverse`, `char_poly_coeffs`, `eigenvalues_from_charpoly`, `nullspace`, `diagonalize`; inverse exclusively by Gauss–Jordan; power identity $A^5=PD^5P^{-1}$ on the $2\times 2$ example.

**Deliverables.** `Project6/22127107.ipynb`, `Project6/Toan UDTK_Project_3-Diagonal matrix.pdf`

---

## Project 7 — Wine-quality OLS

**Objective.** Predict sensory `quality` from eleven physicochemical covariates in `wine.csv` ($n=1199$) by OLS from the normal equations, compared by **five-fold cross-validation**.

**Formulation.** With intercept-augmented $X$,

$$
\hat\beta=\arg\min_\beta\lVert X\beta-y\rVert_2^2,
$$

solved by a numerically stable treatment of $X^\top X\,\hat\beta=X^\top y$ rather than an explicit inverse. Reported metrics: MSE, RMSE, MAE, $R^2$. When a customised design is used, features are standardised **inside each fold** from training moments only.

| Part | Design | Selection rule | Result |
|:----:|:-------|:---------------|:-------|
| (a) | All 11 raw features | — | CV MSE **0.4166** · CV $R^2$ **0.361** |
| (b) | Best univariate model | Minimal 5-fold CV MSE | **alcohol** · CV MSE **0.4887** · CV $R^2$ **0.252** |
| (c) | Forward selection over raw, log, square, and interaction terms | Greedy CV-MSE improvement | 9 terms · CV MSE **0.4007** · CV $R^2$ **0.386** |

The selected custom specification includes `log_alcohol`, `alcohol×volatile acidity`, `alcohol×sulphates`, `sulphates²`, `total sulfur dioxide`, `chlorides`, `alcohol×pH`, and `density`. Relative to (a), (c) reduces CV MSE by about $0.016$ and raises CV $R^2$ by about $0.025$; relative to (b) the gain is larger ($\Delta$ CV MSE $\approx 0.088$). In-sample $R^2$ remains moderate ($\approx 0.40$): `quality` is an ordinal sensory score, so a linear Gaussian model is a first-order approximation, not a generative account of tasting.

**Implementation.** From-scratch OLS, metrics, $k$-fold splitter, and Pearson correlation; documented candidate pool; coefficient table on the standardised scale for (c); no scikit-learn estimator on the fitting path.

**Deliverables.** `Project7/22127107.ipynb`, `Project7/Toan UDTK_Project_4-Linear Regression.pdf`, `Project7/wine.csv`

---

## Final 1 — Markov regimes on the S&P 500

**Objective.** A three-state discrete-time Markov chain on daily log-returns of the S&P 500 (`^GSPC`, 2 January 2019 – 11 August 2026; $n=1911$ returns after cleaning): estimate the kernel, forecast finite-horizon distributions, and compute the stationary law. Libraries handle I/O and graphics only; $\hat P$, $P^t$, and $\pi$ are written from first principles.

**State space.** $R_t=\ln(P_t/P_{t-1})$ is classified from the sample mean $\mu$ and standard deviation $\sigma$:

$$
X_t=
\begin{cases}
0 & \text{(Bear)}, & R_t < \mu-k\sigma,\\
1 & \text{(Sideway)}, & \lvert R_t-\mu\rvert \le k\sigma,\\
2 & \text{(Bull)}, & R_t > \mu+k\sigma,
\end{cases}
\quad k=0.5,
$$

after a sweep over $k\in\{0.25,0.5,1.0\}$. The chosen $k$ yields Bear $21.7\%$, Sideway $53.7\%$, Bull $24.6\%$ — sufficient occupancy in every cell of $N_{ij}$ for a stable MLE.

**Estimated kernel** (row-stochastic):

$$
\hat P
\approx
\begin{pmatrix}
0.2675 & 0.3976 & 0.3349 \\
0.1941 & 0.5912 & 0.2146 \\
0.2213 & 0.5426 & 0.2362
\end{pmatrix}.
$$

Sideway is sticky ($p_{11}\approx 0.59$). From a Bear start, $v_t=v_0\hat P^t$ (binary exponentiation) is already indistinguishable from the stationary law at $t=20$.

**Stationary distribution.** The linear system $\pi(P-I)=0$ with $\sum\pi_i=1$, and the left eigenvector for eigenvalue $1$, agree to $10^{-16}$:

$$
\pi\approx(0.2167,\ 0.5373,\ 0.2460).
$$

Long-run occupancy is dominated by Sideway, with a mild Bull–Bear asymmetry consistent with a positive equity drift.

**Diagnostics.** A second-order memory check compares $P(X_{t+1}\mid X_t)$ with $P(X_{t+1}\mid X_t,X_{t-1})$; mean absolute deviation $\approx 0.052$, largest on the Bear→Sideway path. The first-order Markov hypothesis is a useful approximation, not an exact law. Bonus: a six-state chain $Y_t=2R_t+V_t$ crosses return regime with volume above or below the sample median, attaching a liquidity coordinate to the kernel.

**Deliverables.** `Final 1/22127107-NguyenTheHien.ipynb`, `Final 1/22127107-NguyenTheHien.pdf`, `Final 1/22127107-NguyenTheHien.csv`, `Final 1/Do an cuoi ky.pdf`

---

## Final 2 — Stockton prices and a traffic chain

**Objective.** Two independent problems, both reduced to linear algebra. First, rank OLS predictors of residential selling prices in Stockton, California. Second, estimate a three-state traffic chain from a reproducible 60-day path and compute its $k$-step and stationary distributions.

### Part 1 — Hedonic pricing (`stockton4.csv`, $n=1500$)

Transactions from 1 October 1996 to 30 November 1998 (Knight, University of the Pacific). Response: `sprice` (USD). Covariates: living area (`livarea`, hundreds of ft²), bedrooms, bathrooms, large-lot indicator (`lgelot`, lot $>0.5$ acre), age, pool. Mean price $\$123{,}694$ (median $\$109{,}500$); `sprice` is right-skewed. The strongest linear associate of price is `livarea` ($r\approx 0.79$).

The ranking criterion required by the assignment is the Euclidean residual on the **dollar** scale,

$$
\lVert e\rVert_2=\lVert y-X\hat\theta\rVert_2,
\qquad
(X^\top X)\hat\theta=X^\top y.
$$

Log-linear fits are mapped back by $\hat y=\exp(X\hat\theta)$ before scoring, so every specification is comparable in USD.

| Stage | Specification | $\lVert e\rVert_2$ | RMSE (USD) | $R^2$ |
|:-----:|:--------------|-------------------:|-----------:|------:|
| 1.b | Univariate `livarea` | $1{,}492{,}303$ | $38{,}531$ | $0.629$ |
| 1.c | Linear model, all six covariates | $1{,}353{,}757$ | $34{,}954$ | $0.694$ |
| 1.d | Quadratic area & age + `livarea×lgelot` + `livarea×pool` | **$1{,}312{,}397$** | **$33{,}886$** | **$0.713$** |

Univariate slope on living area is about $\$9{,}182$ per 100 ft² ($\approx \$92$/ft²). In the six-covariate fit, `lgelot` carries a large positive premium ($\$59{,}598$) and `age` a small depreciation; `beds` and `baths` change sign once area is controlled — a collinearity / partition effect, not a causal claim. Residual plots remain heteroscedastic in the upper tail. The preferred model is in-sample: adding terms cannot increase $\lVert e\rVert_2$ on the estimation sample.

### Part 2 — Traffic Markov chain

States $\{\mathrm{K},\mathrm{B},\mathrm{T}\}$ (congested, normal, clear). A length-$60$ path is drawn i.i.d. uniform with seed equal to the student identifier, yielding $59$ observed transitions. The MLE kernel is $\hat p_{ij}=C_{ij}/\sum_{j'}C_{ij'}$. With uninformative $\pi^{(0)}=(1/3,1/3,1/3)$,

$$
\pi^{(k)}=\pi^{(0)}\hat P^k
$$

is tabulated at $k\in\{1,2,3,10\}$. The stationary solver `prop_sta` replaces one row of $(\hat P^\top-I)\pi^\top=0$ by $\sum\pi_i=1$ and attains $\|\pi\hat P-\pi\|_\infty\sim 10^{-16}$. Mixing is rapid: $\pi^{(10)}$ is already indistinguishable from

$$
\pi\approx(0.3557,\ 0.3043,\ 0.3400)
$$

on $(\mathrm{K},\mathrm{B},\mathrm{T})$. Because the path is i.i.d., departures of $\hat P$ from $1/3$ are sampling error; the computational pipeline itself does not assume independence and applies unchanged to a serially dependent traffic record.

**Deliverables.** `Final 2/22127107-nguyenthehien.ipynb`, `Final 2/22127107-nguyenthehien.pdf`, `Final 2/stockton4.csv`, `Final 2/stockton4.def`, `Final 2/Do an cuoi ky.pdf`

---

## Limitations

The following restrictions are part of the scientific record, not defects to be hidden.

- **Course-scale numerics.** Classical Gram–Schmidt and Faddeev–LeVerrier are pedagogically exact and adequate on the demonstration matrices; they are not substitutes for Householder QR or a production eigensolver on ill-conditioned large $A$.
- **In-sample ranking (Final 2, part 1).** The assignment scores $\lVert e\rVert_2$ on the estimation sample. Nested models cannot lose on that criterion; out-of-sample validity is not claimed.
- **Ordinal responses (Project 7).** Sensory `quality` is treated as continuous. A linear Gaussian likelihood is a working approximation.
- **Markov order (Final 1).** The second-order check rejects an exact first-order law. Reported $\pi$ is the stationary law of the fitted first-order kernel, not a claim that markets are Markov.
- **Synthetic traffic path (Final 2, part 2).** The length-$60$ trajectory is generated from the student identifier. The code path is written for a real count matrix; the numerical kernel reflects sampling error around $1/3$.
- **No causal identification.** Sign changes on `beds`/`baths` after controlling for area, and regime labels on equity returns, are descriptive.

---

## Environment and reproduction

**Stack.** Python 3.10+; `numpy`, `pandas`, `matplotlib`; `seaborn` (Projects 1–3); `scikit-learn` (Project 3 only); `pillow` (Projects 1–2); `tabulate` (Project 3 tables); Jupyter Notebook or JupyterLab.

Projects 4–7 and both dissertations fit linear systems, factor matrices, and estimate Markov kernels **without** scikit-learn estimators.

```bash
# Laboratory sequence
jupyter notebook "Project 1/Lab1.ipynb"
jupyter notebook Project2/Lab2.ipynb
jupyter notebook Project3/Lab3.ipynb     # train.csv and test.csv beside the notebook

# Computational linear algebra
jupyter notebook Project4/22127107.ipynb
jupyter notebook Project5/22127107.ipynb
jupyter notebook Project6/22127107.ipynb
jupyter notebook Project7/22127107.ipynb # wine.csv beside the notebook

# Dissertations
jupyter notebook "Final 1/22127107-NguyenTheHien.ipynb"   # CSV beside the notebook
jupyter notebook "Final 2/22127107-nguyenthehien.ipynb"   # stockton4.csv beside the notebook
```

Execute cells from top to bottom. Data files must remain in the same directory as the notebook that reads them. Expected residuals and CV scores are those printed by the notebooks at the time of submission; floating-point values may differ in the last digits across BLAS implementations.

---

## Report convention

Each PDF follows a fixed scholarly skeleton:

1. Cover (institution, course, author, instructors)
2. Abstract / acknowledgements where required
3. Mathematical preliminaries
4. Implementation notes and experimental protocol
5. Results (tables, figures, numbered formulae)
6. Discussion and limitations
7. References

Equations are stated before they are coded. Metrics are defined before they are tabulated. Initialisation, shuffle seeds, fold protocol, state thresholds, and RNG seeds are recorded for regeneration.

---

## Academic integrity

All notebooks and reports in this repository are the coursework of **Nguyễn Thế Hiển (22127107)**. Implementations observe the constraints of each assignment (permitted libraries, required signatures, prescribed metrics). External sources used for theory or tooling are cited in the corresponding PDF. This archive is submitted as evidence of independent work, not as a third-party solution set.

---

## How to cite

If this archive is referenced (for example in a later report or a related project), use:

> Nguyễn Thế Hiển. (2026). *Applied Mathematics and Statistics for Information Technology* (MTH00051 coursework archive, student 22127107). Faculty of Information Technology, University of Science, VNU–HCM. https://github.com/TheHien04/Applied-mathematics-and-statistics-for-IT

```bibtex
@misc{hien2026mth00051,
  author       = {Nguyễn Thế Hiển},
  title        = {Applied Mathematics and Statistics for Information Technology},
  year         = {2026},
  howpublished = {Coursework archive, MTH00051, University of Science, VNU--HCM},
  note         = {Student ID 22127107},
  url          = {https://github.com/TheHien04/Applied-mathematics-and-statistics-for-IT}
}
```

Primary results should be cited from the project PDF when a page-level reference is needed.

---

## Instructors

- Teacher: Võ Nam Thục Đoan
- Teacher: Đinh Ngọc Thanh
- Teacher: Nguyễn Hữu Toàn

---

## References

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
2. Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987–1007.
3. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.
4. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.
5. Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357–384.
6. Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.
7. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.
8. Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to Linear Regression Analysis* (6th ed.). Wiley.
9. Norris, J. R. (1998). *Markov Chains*. Cambridge University Press.
10. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
11. Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press.
12. Tsay, R. S. (2010). *Analysis of Financial Time Series* (3rd ed.). Wiley.

Full bibliographic lists appear in the individual reports.

---

<p align="center">
  <sub>MTH00051 · Applied Mathematics and Statistics · Faculty of Information Technology · University of Science, VNU–HCM · 2024–2026</sub>
</p>
