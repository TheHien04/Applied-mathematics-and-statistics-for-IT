# Applied Mathematics and Statistics for IT

**Course:** MTH00051 — Applied Mathematics and Statistics  
**Institution:** Faculty of Information Technology, University of Science, VNU–HCM  
**Student:** Nguyễn Thế Hiển · `22127107` · Class `22CLC08`

This repository collects three practical projects from MTH00051. Each project links a classical mathematical idea—clustering in Euclidean space, discrete image operators as linear maps, and ordinary least squares under cross-validation—to a reproducible Python implementation and an academic report.

---

## Mathematical Scope

| Project | Core theme | Mathematical objects | Learning outcome |
|:-------:|:-----------|:---------------------|:-----------------|
| **1** | Unsupervised color quantization | $k$-means on RGB vectors in $\mathbb{R}^3$; empirical risk minimization | Prototype-based clustering and palette compression |
| **2** | Digital image processing | Pointwise maps; geometric transforms; discrete 2D convolution | Linear-algebraic view of filtering and geometry |
| **3** | Supervised linear prediction | OLS, MAE, $K$-fold cross-validation | Model selection and error estimation for regression |

Across the three projects, the emphasis is on **transparent mathematics**, **correct numerical realization**, and **report-level documentation** rather than black-box library pipelines.

---

## Repository Structure

```text
.
├── README.md
├── Project 1/
│   ├── Lab1.ipynb          # K-Means color compression
│   └── Lab1.pdf            # Academic practical report
├── Project2/
│   ├── Lab2.ipynb          # Image processing toolbox
│   └── Lab2.pdf            # Academic practical report
└── Project3/
    ├── Lab3.ipynb          # Linear regression experiments
    ├── Lab3.pdf            # Academic practical report
    ├── train.csv           # Training split (9,000 samples)
    └── test.csv            # Held-out test split (1,000 samples)
```

Each folder is self-contained: the notebook is the computational artifact; the PDF is the formal write-up (problem statement, theory, method, experiments, discussion, references).

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

## Environment & Reproduction

**Suggested stack**

- Python 3.10+
- `numpy`, `pandas`, `matplotlib`, `seaborn`
- `scikit-learn` (Project 3)
- `pillow` (Projects 1–2)
- `tabulate` (Project 3 tables)
- Jupyter Notebook / JupyterLab

**Run a project**

```bash
# Project 1
jupyter notebook "Project 1/Lab1.ipynb"

# Project 2
jupyter notebook Project2/Lab2.ipynb

# Project 3 (CSV files must sit beside the notebook)
jupyter notebook Project3/Lab3.ipynb
```

Execute cells top-to-bottom. For Project 3, ensure `train.csv` and `test.csv` remain in `Project3/`.

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

Reports are written for an applied mathematics and statistics audience: equations are stated explicitly, metrics are defined before use, and experimental choices (initialization, shuffle seed, fold protocol) are recorded for reproducibility.

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
5. Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.  
6. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830.

Full bibliographic lists appear in each project report.

---

<p align="center">
  <sub>MTH00051 · Applied Mathematics and Statistics · University of Science, VNU–HCM · 2024</sub>
</p>
