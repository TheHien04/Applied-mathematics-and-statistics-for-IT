# Applied Mathematics and Statistics for IT

**Course:** MTH00051 — Applied Mathematics and Statistics  
**Institution:** Faculty of Information Technology, University of Science, VNU–HCM  
**Student:** Nguyễn Thế Hiển · `22127107` · Class `22CLC08`

This repository collects seven practical projects and two final dissertations from the applied mathematics and statistics curriculum. Each artefact links a classical mathematical idea—clustering in Euclidean space, discrete image operators, Gaussian elimination, Gram–Schmidt orthogonalization, matrix diagonalization, ordinary least squares, and finite Markov chains—to a reproducible Python implementation and an academic report.

---

## Mathematical Scope

| Item | Core theme | Mathematical objects | Learning outcome |
|:----:|:-----------|:---------------------|:-----------------|
| **1** | Unsupervised color quantization | $k$-means on RGB vectors in $\mathbb{R}^3$; empirical risk minimization | Prototype-based clustering and palette compression |
| **2** | Digital image processing | Pointwise maps; geometric transforms; discrete 2D convolution | Linear-algebraic view of filtering and geometry |
| **3** | Supervised linear prediction | OLS, MAE, $K$-fold cross-validation | Model selection and error estimation for regression |
| **4** | Direct solution of linear systems | Gaussian elimination with partial pivoting; back substitution | Existence, uniqueness, and constructive solution of $Ax=b$ |
| **5** | Orthogonal factorization | Classical Gram–Schmidt; $A=QR$ | Orthonormal bases and numerically usable triangular factors |
| **6** | Spectral factorization | Characteristic polynomial; eigenpairs; $A=PDP^{-1}$ | Diagonalization via Gauss–Jordan inversion |
| **7** | Multivariate OLS on physicochemical data | Normal equations; 5-fold CV; forward selection | Feature design and out-of-sample comparison of regressors |
| **F1** | Discrete-time Markov market regimes | Stochastic kernel $\hat P$; $v_t=v_0P^t$; stationary $\pi$ | Regime classification, forecast, and first-order Markov diagnostics |
| **F2** | Hedonic pricing and a traffic chain | OLS residual norm; polynomial / interaction designs; finite Markov kernel | In-sample model ranking and Chapman–Kolmogorov evolution |

Across all items, the emphasis is on **transparent mathematics**, **correct numerical realization from defining equations**, and **report-level documentation** rather than black-box library pipelines. Library solvers (`numpy.linalg.solve`, `numpy.linalg.qr`, `numpy.linalg.eig`) appear only as independent numerical checks.

---

## Repository Structure

```text
.
├── README.md
├── Project 1/
│   ├── Lab1.ipynb                              # K-Means color compression
│   └── Lab1.pdf                                # Academic practical report
├── Project2/
│   ├── Lab2.ipynb                              # Image processing toolbox
│   └── Lab2.pdf                                # Academic practical report
├── Project3/
│   ├── Lab3.ipynb                              # Linear regression experiments
│   ├── Lab3.pdf                                # Academic practical report
│   ├── train.csv                               # Training split (9,000 samples)
│   └── test.csv                                # Held-out test split (1,000 samples)
├── Project4/
│   └── 22127107.ipynb                          # Gaussian elimination
├── Project5/
│   ├── 22127107.ipynb                          # Gram–Schmidt QR
│   └── Toan UDTK_Project_2-Gram-Schmidt.pdf    # Assignment brief
├── Project6/
│   ├── 22127107.ipynb                          # Matrix diagonalization
│   └── Toan UDTK_Project_3-Diagonal matrix.pdf
├── Project7/
│   ├── 22127107.ipynb                          # Wine-quality OLS
│   ├── Toan UDTK_Project_4-Linear Regression.pdf
│   └── wine.csv                                # n = 1,199 physicochemical samples
├── Final 1/
│   ├── 22127107-NguyenTheHien.ipynb            # S&P 500 Markov regimes
│   ├── 22127107-NguyenTheHien.pdf              # Academic report
│   ├── 22127107-NguyenTheHien.csv              # Daily OHLCV (^GSPC)
│   └── Do an cuoi ky.pdf                       # Final assignment brief
└── Final 2/
    ├── 22127107-nguyenthehien.ipynb            # Stockton prices + traffic chain
    ├── 22127107-nguyenthehien.pdf
    ├── Do an cuoi ky.pdf
    ├── stockton4.csv                           # n = 1,500 residential sales
    └── stockton4.def                           # Variable dictionary
```

Each folder is self-contained: the notebook is the computational artefact; the PDF is the formal write-up (problem statement, theory, method, experiments, discussion, references). Assignment briefs are kept beside the solutions where they were issued.

---

## Project 1 — Color Compression via $k$-Means

**Objective.** Represent an RGB image with a reduced palette of $k$ colors by clustering pixels and replacing each pixel by its cluster centroid.

**Mathematical formulation.** Treat each pixel as a vector $x_i \in \{0,\ldots,255\}^3 \subset \mathbb{R}^3$. The $k$-means objective seeks centroids $\mu_1,\ldots,\mu_k$ and assignments $c_i \in \{1,\ldots,k\}$ minimizing

$$
J = \sum_{i=1}^{n} \bigl\| x_i - \mu_{c_i} \bigr\|_2^2.
$$

Iterations alternate between nearest-centroid assignment and centroid update (sample means). Initialization may be random or based on in-pixels; convergence is monitored by centroid displacement (e.g., `numpy.allclose`).

**Implementation highlights.**
- RGB conversion and vectorized pixel matrix construction
- Full $k$-means loop with documented helpers
- Compression experiments for $k \in \{3,5,7\}$ under multiple initializations
- Export of reconstructed images and quantitative discussion (e.g., MSE / visual fidelity)

**Deliverables:** `Project 1/Lab1.ipynb`, `Project 1/Lab1.pdf`

---

## Project 2 — Image Processing

**Objective.** Implement a coherent toolbox of elementary digital image operators under course constraints (NumPy / Pillow / Matplotlib; no black-box filtering shortcuts).

**Mathematical families.**

1. **Pointwise transforms** — brightness, contrast, grayscale (ITU-R BT.601 luma), sepia as an affine map in RGB.
2. **Geometric transforms** — flip, center crop, elliptical / double-ellipse masks (with rotation angle $\alpha$), bilinear resize.
3. **Linear filtering** — same-size 2D convolution with edge padding,

$$
(I * K)(x,y) = \sum_{i=-a}^{a}\sum_{j=-b}^{b} K(i,j)\, I(x-i,y-j),
$$

used for box blur and sharpening on each channel.

**Implementation highlights.**
- Explicit `_convolve2d` (true spatial 2D convolution, not 1D convolution on a flattened raster)
- Docstrings for every required operator
- Interactive `main` with per-operator and apply-all modes
- Saved visual outputs for each transform

**Deliverables:** `Project2/Lab2.ipynb`, `Project2/Lab2.pdf`

---

## Project 3 — Linear Regression

**Objective.** Predict **Student Performance Index** from five academic / lifestyle features using ordinary least squares (OLS), with model selection by cross-validated mean absolute error (MAE).

**Features.** Hours Studied, Previous Scores, Extracurricular Activities, Sleep Hours, Sample Question Papers Practiced.  
**Target.** Performance Index (continuous).  
**Data.** `train.csv` ($n=9000$), `test.csv` ($n=1000$).

**Mathematical formulation.** For design matrix $X$ and target $y$,

$$
\hat{y} = X\hat{w}, \qquad
\hat{w} = \arg\min_w \|Xw - y\|_2^2,
$$

with evaluation metric

$$
\mathrm{MAE} = \frac{1}{n}\sum_{i=1}^{n} |y_i - \hat{y}_i|.
$$

Model selection uses **5-fold cross-validation** after shuffling the training set **exactly once**, scoring mean validation MAE.

**Requirements covered.**

| Req. | Task | Selected model | Key metric |
|:----:|:-----|:---------------|:-----------|
| 1 | Exploratory data analysis (train only) | — | correlations, distributions, missingness |
| 2a | OLS with all 5 features | full model | test MAE **1.596** |
| 2b | Best single feature via 5-fold CV | Previous Scores | CV MAE **6.6182** · test MAE **6.5443** |
| 2c | Custom designs via same CV protocol | Hours + Previous + Sleep | CV MAE **1.7021** · test MAE **1.6943** |

**Implementation highlights.**
- Documented helpers: `mae`, `regression_formula`, `design_matrix`
- Single shared shuffle for all CV experiments (2b and 2c)
- Explicit regression formulas with coefficients rounded to three decimals
- English notebook aligned with the academic report

**Deliverables:** `Project3/Lab3.ipynb`, `Project3/Lab3.pdf`, `Project3/train.csv`, `Project3/test.csv`

---

## Project 4 — Gaussian Elimination

**Objective.** Solve a linear system $Ax=b$ by elementary row operations, without calling a black-box linear solver for the student implementation.

**Mathematical formulation.** Form the augmented matrix $[A\mid b]$ and reduce it to row-echelon form. At column $i$, partial pivoting selects the row of largest absolute entry on or below the diagonal; the pivot row is scaled to $1$ and entries below the pivot are annihilated. Back substitution then recovers $x$ from the triangular system. The algorithm reports the three classical alternatives:

- unique solution, when $\operatorname{rank}(A)=\operatorname{rank}([A\mid b])=n$;
- no solution, when a zero row of $A$ faces a nonzero right-hand side;
- infinitely many solutions, when the rank is strictly less than the number of unknowns.

**Worked example.** For

$$
\begin{aligned}
x+y+z &= 6,\\
2y+5z &= -4,\\
2x+5y-z &= 27,
\end{aligned}
$$

the implementation returns $x=(5,3,-2)$, in agreement with `numpy.linalg.solve`.

**Implementation highlights.**
- `Gauss_elimination(A)` — forward elimination with partial pivoting on a list-of-lists augmented matrix
- `back_substitution(A)` — uniqueness / inconsistency / under-determination diagnostics
- Independent numerical check against NumPy (not used inside the student solver)

**Deliverables:** `Project4/22127107.ipynb`

---

## Project 5 — Gram–Schmidt QR Decomposition

**Objective.** Factor a full-column-rank matrix $A\in\mathbb{R}^{m\times n}$ as $A=QR$ by the classical Gram–Schmidt process, then verify orthonormality and reconstruction.

**Mathematical formulation.** Writing $A=[a_1,\ldots,a_n]$, the $k$-th orthonormal column is obtained by subtracting the already computed projections and normalizing:

$$
u_k = a_k - \sum_{j=1}^{k-1} (q_j^\top a_k)\, q_j,
\qquad
q_k = \frac{u_k}{\lVert u_k\rVert_2}.
$$

The upper-triangular factor is $R=Q^\top A$. Linear dependence is detected when $\lVert u_k\rVert_2=0$. Complexity of the classical algorithm is $O(mn^2)$. Sign patterns of $(Q,R)$ need not match Householder QR; the invariant is $QR=A$ and $Q^\top Q=I_n$.

**Empirical checks.**
- Square example $A\in\mathbb{R}^{3\times 3}$: $A\approx QR$ and $Q^\top Q\approx I$ both hold.
- Tall example $A_2\in\mathbb{R}^{3\times 2}$: the same identities hold.
- Against `numpy.linalg.qr`: reconstruction error $\|A-QR\|_\infty \approx 7.56\times 10^{-16}$.

**Implementation highlights.**
- Single routine `gram_schmidt_qr(A)` with an explicit rank-deficiency error
- No library QR inside the student factorization
- Discussion of least-squares, eigenvalue iterations, and numerical stability relative to modified Gram–Schmidt / Householder

**Deliverables:** `Project5/22127107.ipynb`, `Project5/Toan UDTK_Project_2-Gram-Schmidt.pdf`

---

## Project 6 — Diagonalizable Matrices

**Objective.** For a diagonalizable square matrix $A$, construct $P$, $D$, and $P^{-1}$ such that $A=PDP^{-1}$, using only course-level linear algebra (no library eigendecomposition inside the student pipeline).

**Mathematical formulation.**

1. Coefficients of the characteristic polynomial $\det(\lambda I-A)$ are obtained by the Faddeev–LeVerrier recurrence; roots are the eigenvalues $\lambda_i$.
2. For each $\lambda_i$, a basis of $\ker(A-\lambda_i I)$ is extracted from the RREF of the homogeneous system.
3. Columns of $P$ are the eigenvectors; $D=\operatorname{diag}(\lambda_1,\ldots,\lambda_n)$.
4. $P^{-1}$ is computed by Gauss–Jordan reduction of $[P\mid I]$. Reconstruction is $\hat A=PDP^{-1}$.

A standard application is fast powers: $A^k=PD^k P^{-1}$.

**Empirical checks.**

| Matrix | Eigenvalues (student) | $\|A-PDP^{-1}\|$ | NumPy reconstruction |
|:------:|:----------------------|:----------------:|:---------------------|
| $A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$ | $2,3$ | $0$ | $\approx 1.11\times 10^{-16}$ |
| $A_2\in\mathbb{R}^{3\times 3}$ | $1,2,3$ | $\approx 1.29\times 10^{-15}$ | consistent |

Eigenvectors may differ from `numpy.linalg.eig` by scaling and sign; the comparison criterion is reconstruction of $A$, not entrywise equality of $P$.

**Implementation highlights.**
- Helpers: `rref`, `gauss_jordan_inverse`, `char_poly_coeffs`, `eigenvalues_from_charpoly`, `nullspace`, `diagonalize`
- Inverse computed exclusively by Gauss–Jordan
- Power identity $A^5=PD^5P^{-1}$ verified on the $2\times 2$ example

**Deliverables:** `Project6/22127107.ipynb`, `Project6/Toan UDTK_Project_3-Diagonal matrix.pdf`

---

## Project 7 — Linear Regression for Wine Quality

**Objective.** Predict sensory `quality` from eleven physicochemical covariates in `wine.csv` ($n=1199$) by OLS implemented from the normal equations, with model comparison by **5-fold cross-validation**.

**Mathematical formulation.** With intercept-augmented design $X$ and response $y$,

$$
\hat\beta = \arg\min_\beta \lVert X\beta-y\rVert_2^2,
$$

solved via a numerically stable linear solve of $X^\top X\,\hat\beta=X^\top y$ rather than an explicit inverse. Reported metrics are MSE, RMSE, MAE, and $R^2$. Cross-validation standardizes features **inside each fold** (train moments only) whenever a customized design is used, to avoid leakage.

**Protocol.**

| Part | Design | Selection rule | Result |
|:----:|:-------|:---------------|:-------|
| (a) | All 11 raw features | — | CV MSE **0.4166** · CV $R^2$ **0.361** |
| (b) | Best univariate model | minimal 5-fold CV MSE | **alcohol** · CV MSE **0.4887** · CV $R^2$ **0.252** |
| (c) | Forward selection over raw, log, square, and interaction terms | greedy CV-MSE improvement | 9 terms · CV MSE **0.4007** · CV $R^2$ **0.386** |

The selected custom specification includes `log_alcohol`, `alcohol×volatile acidity`, `alcohol×sulphates`, `sulphates²`, `total sulfur dioxide`, `chlorides`, `alcohol×pH`, and `density`. Relative to (a), part (c) reduces CV MSE by about $0.016$ and raises CV $R^2$ by about $0.025$; relative to (b) the gains are larger ($\Delta$CV MSE $\approx 0.088$). In-sample $R^2$ remains moderate ($\approx 0.40$): quality is an ordinal sensory score, so a linear Gaussian model is a first-order approximation rather than a complete generative description.

**Implementation highlights.**
- From-scratch OLS, metrics, $k$-fold splitter, and Pearson correlation
- Forward selection with a documented candidate pool (nonlinear and interaction terms)
- Coefficient table on the standardized scale for part (c)
- No scikit-learn estimators in the fitting path

**Deliverables:** `Project7/22127107.ipynb`, `Project7/Toan UDTK_Project_4-Linear Regression.pdf`, `Project7/wine.csv`

---

## Final 1 — Markov Modelling of S&P 500 Market Regimes

**Objective.** Construct a three-state discrete-time Markov chain on daily log-returns of the S&P 500 (`^GSPC`, 2 January 2019 – 11 August 2026; $n=1911$ returns after cleaning), estimate the transition kernel, forecast finite-horizon distributions, and compute the stationary law. Libraries are used only for I/O and graphics; $\hat P$, $P^t$, and $\pi$ are implemented from first principles.

**State space.** Log-return $R_t=\ln(P_t/P_{t-1})$ is classified by sample mean $\mu$ and sample standard deviation $\sigma$:

$$
X_t=
\begin{cases}
0 & \text{(Bear)}, & R_t < \mu-k\sigma,\\
1 & \text{(Sideway)}, & \lvert R_t-\mu\rvert \le k\sigma,\\
2 & \text{(Bull)}, & R_t > \mu+k\sigma,
\end{cases}
\quad k=0.5
$$

after a sensitivity sweep over $k\in\{0.25,0.5,1.0\}$. The chosen $k$ yields Bear $21.7\%$, Sideway $53.7\%$, Bull $24.6\%$ — enough occupancy in every cell of $N_{ij}$ for a stable MLE.

**Estimated kernel** (row-stochastic; $\hat p_{ij}=N_{ij}/\sum_k N_{ik}$):

$$
\hat P
\approx
\begin{pmatrix}
0.2675 & 0.3976 & 0.3349 \\
0.1941 & 0.5912 & 0.2146 \\
0.2213 & 0.5426 & 0.2362
\end{pmatrix}.
$$

Sideway is sticky ($p_{11}\approx 0.59$). Starting from Bear, $v_t=v_0\hat P^t$ (binary exponentiation) is already indistinguishable from the stationary law at $t=20$.

**Stationary distribution.** Two independent solvers — the linear system $\pi(P-I)=0$ with $\sum\pi_i=1$, and the left eigenvector for eigenvalue $1$ — agree to $10^{-16}$:

$$
\pi \approx (0.2167,\ 0.5373,\ 0.2460).
$$

Long-run occupancy is therefore dominated by Sideway, with a mild Bull–Bear asymmetry consistent with a positive equity drift.

**Diagnostics and extension.**
- A second-order memory check compares $P(X_{t+1}\mid X_t)$ with $P(X_{t+1}\mid X_t,X_{t-1})$; mean absolute deviation $\approx 0.052$, largest on the Bear→Sideway path — the first-order Markov hypothesis is a useful approximation, not an exact law.
- Bonus: a six-state chain $Y_t=2R_t+V_t$ crosses return regime with volume above/below the sample median, attaching a liquidity coordinate to the kernel.

**Deliverables:** `Final 1/22127107-NguyenTheHien.ipynb`, `Final 1/22127107-NguyenTheHien.pdf`, `Final 1/22127107-NguyenTheHien.csv`, `Final 1/Do an cuoi ky.pdf`

---

## Final 2 — Stockton House Prices and a Finite Traffic Chain

**Objective.** Two independent quantitative problems, both reduced to linear algebra. First, rank OLS predictors of residential selling prices in Stockton, California. Second, estimate a three-state traffic Markov chain from a reproducible 60-day path and compute its $k$-step and stationary distributions.

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

States $\{\mathrm{K},\mathrm{B},\mathrm{T}\}$ (congested, normal, clear). A length-$60$ path is drawn i.i.d. uniform with seed equal to the student identifier, yielding $59$ observed transitions. The MLE kernel is the row normalisation $\hat p_{ij}=C_{ij}/\sum_{j'}C_{ij'}$. With uninformative $\pi^{(0)}=(1/3,1/3,1/3)$,

$$
\pi^{(k)}=\pi^{(0)}\hat P^k
$$

is tabulated at $k\in\{1,2,3,10\}$. The stationary solver `prop_sta` replaces one row of $(\hat P^\top-I)\pi^\top=0$ by $\sum\pi_i=1$ and attains $\|\pi\hat P-\pi\|_\infty\sim 10^{-16}$. Mixing is rapid: $\pi^{(10)}$ is already indistinguishable from

$$
\pi \approx (0.3557,\ 0.3043,\ 0.3400)
$$

on $(\mathrm{K},\mathrm{B},\mathrm{T})$. Because the path is i.i.d., departures of $\hat P$ from $1/3$ are sampling error; the computational pipeline itself does not assume independence and applies unchanged to a serially dependent traffic record.

**Deliverables:** `Final 2/22127107-nguyenthehien.ipynb`, `Final 2/22127107-nguyenthehien.pdf`, `Final 2/stockton4.csv`, `Final 2/stockton4.def`, `Final 2/Do an cuoi ky.pdf`

---

## Environment & Reproduction

**Suggested stack**

- Python 3.10+
- `numpy`, `pandas`, `matplotlib`
- `seaborn` (Projects 1–3)
- `scikit-learn` (Project 3 only)
- `pillow` (Projects 1–2)
- `tabulate` (Project 3 tables)
- Jupyter Notebook / JupyterLab

Projects 4–7 and both finals fit and invert linear systems, factor matrices, and estimate Markov kernels **without** scikit-learn estimators.

**Run a project**

```bash
# Projects 1–3
jupyter notebook "Project 1/Lab1.ipynb"
jupyter notebook Project2/Lab2.ipynb
jupyter notebook Project3/Lab3.ipynb     # train.csv and test.csv must sit beside the notebook

# Projects 4–7
jupyter notebook Project4/22127107.ipynb
jupyter notebook Project5/22127107.ipynb
jupyter notebook Project6/22127107.ipynb
jupyter notebook Project7/22127107.ipynb # wine.csv must sit beside the notebook

# Final dissertations
jupyter notebook "Final 1/22127107-NguyenTheHien.ipynb"   # CSV beside the notebook
jupyter notebook "Final 2/22127107-nguyenthehien.ipynb"   # stockton4.csv beside the notebook
```

Execute cells top-to-bottom. Data files must remain in the same folder as the notebook that reads them.

---

## Report Convention

Each PDF follows a consistent academic structure:

1. Cover (institution, course, student, instructors)
2. Abstract / acknowledgments (as applicable)
3. Mathematical preliminaries
4. Implementation notes and experimental protocol
5. Results (tables, figures, formulas)
6. Discussion and limitations
7. References

Reports are written for an applied mathematics and statistics audience: equations are stated explicitly, metrics are defined before use, and experimental choices (initialization, shuffle seed, fold protocol, state thresholds, RNG seed) are recorded for reproducibility.

---

## Academic Integrity

All notebooks and reports in this repository are the coursework of **Nguyễn Thế Hiển (22127107)**. Implementations follow the course constraints for each project (permitted libraries, required function signatures, and evaluation metrics). External references used for theory or tooling are cited in the corresponding PDF.

---

## Instructors

- Mr. Vũ Quốc Hoàng  
- Mr. Nguyễn Văn Quang Huy  
- Mr. Nguyễn Ngọc Toàn  
- Mrs. Phan Thị Phương Uyên  

---

## References (selected)

1. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.  
2. Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to Linear Regression Analysis* (6th ed.). Wiley.  
3. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.  
4. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.  
5. Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press.  
6. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.  
7. Norris, J. R. (1998). *Markov Chains*. Cambridge University Press.  
8. Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357–384.  
9. Tsay, R. S. (2010). *Analysis of Financial Time Series* (3rd ed.). Wiley.  
10. Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987–1007.  
11. Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.  
12. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830.

Full bibliographic lists appear in each project report.

---

<p align="center">
  <sub>MTH00051 · Applied Mathematics and Statistics · University of Science, VNU–HCM · 2024–2026</sub>
</p>
