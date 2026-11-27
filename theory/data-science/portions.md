# IDSE Theory Topics and Numerical Practice

The combined portion below is based on both faculty folders, including the embedded VK lessons. The folders contain 9 HTML lectures, 5 PowerPoint decks, and 3 introductory PDFs.

## A. Topics and subtopics to learn

| Topic | Subtopics |
|---|---|
| **1. Introduction to data science** | Definition and applications, programming/statistics/domain knowledge, problem definition, data collection, primary versus secondary data, structured/semi-structured/unstructured data, data science workflow, model evaluation, deployment and monitoring, data quality, misleading correlations and model drift. |
| **2. Python fundamentals** | Interpreter versus compiler, variables, datatypes, operators, type conversion, floating-point precision, input/output, objects and identity, mutability, strings and formatting, lists/tuples/sets/dictionaries, copying and aliasing. |
| **3. Control flow and functions** | Truthiness, Boolean precedence and short-circuiting, conditions, loops, range/enumerate/zip, break/continue/pass, loop else, functions and returns, positional/keyword/default arguments, *args/**kwargs, scope, mutable defaults, recursion, lambda, exceptions, modules and packages. |
| **4. NumPy** | Why arrays are efficient, homogeneous dtype, constructors, shape/size/ndim/itemsize/nbytes, indexing and slicing, vectorization, broadcasting, Boolean masks, aggregation and axes, reshaping/transposing/flattening, concatenation/splitting, views versus copies, random generation, matrix operations, NaN handling. |
| **5. Pandas** | Series versus DataFrame, constructors, file input/output, inspection, indexes and alignment, loc/iloc, selection and assignment, filtering, missing values, types and strings, duplicates, renaming/dropping, map/apply, grouping/aggregation/transform, sorting, ranking, merging and concatenation. |
| **6. Data preparation** | Missing-value strategies, inconsistent values and formats, duplicates, outliers, min–max normalization, standardization, aggregation, binning/discretization, log transformations, feature engineering and data reduction. |
| **7. Descriptive statistics** | Mean/median/mode, weighted mean, frequency-table summaries, range, population/sample variance, SD, coefficient of variation, skewness, percentiles/quartiles/IQR, z-scores, boxplots, outlier interpretation. |
| **8. Measurement scales and EDA** | Nominal/ordinal/interval/ratio scales, valid comparisons and summaries, univariate/bivariate/multivariate analysis, covariance, Pearson correlation, Spearman correlation, confounding, correlation versus causation, Simpson’s paradox. |
| **9. Visualization** | Choosing and interpreting plots, histogram bins, line/bar/scatter plots, boxplots and multivariable displays, Matplotlib figures/subplots, titles/labels/legends, styles and saving figures. |
| **10. Probability and distributions** | Discrete/continuous variables, PMF/PDF/CDF, expected value and variance, Bernoulli, binomial, geometric, Poisson, exponential and normal distributions, assumptions, parameters, probability calculations and choosing a model from a scenario. |
| **11. Sampling and inference** | Population/sample, parameters/statistics, representative sampling, sampling bias, sampling distribution of the mean, Central Limit Theorem, standard error, normal approximation for sample means and central 95% ranges. |
| **12. Hypothesis testing** | Null/alternative hypotheses, significance level, null distribution, test statistic, p-value, one-/two-sided tests, reject/fail-to-reject decisions, Type I/II errors, exact binomial tests and known-population-SD one-sample z-tests. |
| **13. Encoding and text features** | Nominal/ordinal categories, label/ordinal/one-hot/binary/frequency/target/hash encoding, advantages and limitations, collisions and leakage, tokenization, vocabulary, document-term matrix, binary/count BoW, unigrams/bigrams/trigrams, TF/DF/IDF/TF-IDF. |
| **14. ML and scikit-learn basics** | Supervised/unsupervised/reinforcement learning, classification versus regression, binary/multiclass classification, features/target, train/test split, scaling, fit/transform/predict, accuracy. JK includes a short KNN API example. |
| **15. Linear regression** | Simple/multiple regression, slope/intercept, residuals, least squares and its derivation, normal equations, design matrix, SSE/SST/MSE, mean baseline, R², coefficient interpretation, outliers, multicollinearity and limitations. |
| **16. Logistic regression** | Binary prediction, odds/log-odds, linear score, sigmoid, likelihood, cross-entropy, gradient derivation and coefficient updates, learning rate, convergence, Newton’s method overview, thresholds, false alarms/misses, accuracy, odds ratios and pseudo-R². |
| **17. K-means** | Centroids, Euclidean distance, assignment/update algorithm, inertia, convergence, local solutions, initialization, K-means++, repeated starts, elbow method, scaling, outlier sensitivity, cluster-shape limitations and image compression. |
| **18. SVM** | Hyperplane, decision score, support vectors, maximum margin, separating-line geometry, hard-margin objective/constraints and derivation, support-vector equations, classifying new points, linear/nonlinear models, linear/polynomial/RBF/sigmoid kernels, gamma and limitations. |
| **19. SVR** | Continuous prediction, epsilon tube, epsilon-insensitive loss, penalty C, objective function, constraints, finding weights/bias and predicting new points. |

**PCA:** No dedicated PCA deck is currently supplied. The faculty screenshot marks it “Coming soon.” If confirmed for the exam, revise centering/scaling, covariance matrices, eigenvalues/eigenvectors, principal components, projection and explained variance.

## B. Numerical topics to practise separately

### 1. Scaling, transformation and binning

Practise min–max normalization, standardization, interval assignment and log transformations.

\[
x_{\text{scaled}}=\frac{x-x_{\min}}{x_{\max}-x_{\min}},
\qquad z=\frac{x-\mu}{\sigma}
\]

### 2. Descriptive statistics

Calculate mean, median, mode, weighted mean, variance, SD and CV, including from frequency tables.

\[
\bar x=\frac{\sum f_ix_i}{\sum f_i},
\qquad \text{weighted mean}=\frac{\sum w_ix_i}{\sum w_i}
\]

\[
s^2=\frac{\sum(x_i-\bar x)^2}{n-1},
\qquad s=\sqrt{s^2},
\qquad CV=\frac{s}{\bar x}\times100\%
\]

Use denominator n for population variance.

### 3. Quartiles, percentiles and outliers

Find Q1/Q2/Q3, IQR, fences, z-scores and percentile ranks. Follow the percentile convention specified in the question.

\[
IQR=Q_3-Q_1
\]

\[
\text{Fences}=Q_1-1.5IQR,\quad Q_3+1.5IQR
\]

### 4. Covariance and correlation

Calculate covariance, Pearson correlation and Spearman rank correlation. Interpret the sign and strength.

\[
r=\frac{\sum(x_i-\bar x)(y_i-\bar y)}
{\sqrt{\sum(x_i-\bar x)^2\sum(y_i-\bar y)^2}}
\]

With no tied ranks:

\[
\rho=1-\frac{6\sum d_i^2}{n(n^2-1)}
\]

Also practise explaining Simpson’s paradox using subgroup and combined percentages.

### 5. Distribution probabilities

| Distribution | Calculation pattern |
|---|---|
| **Bernoulli** | P(X=1)=p, mean p, variance p(1−p) |
| **Binomial** | P(X=k)=C(n,k)pᵏ(1−p)ⁿ⁻ᵏ, mean np, variance np(1−p) |
| **Poisson** | P(X=k)=e⁻λ λᵏ/k!, mean and variance λ |
| **Geometric** | P(X=k)=(1−p)ᵏ⁻¹p, P(X>k)=(1−p)ᵏ, mean 1/p |
| **Exponential** | P(T>t)=e⁻λᵗ, mean 1/λ |
| **Normal** | Convert to z=(x−μ)/σ, then calculate the required area |

Practise exactly, at most, at least, more than, between, expected frequencies, and converting time units consistently.

### 6. CLT and standard error

Calculate probabilities involving sample means, central 95% ranges and changes in precision with sample size.

\[
SE=\frac{\sigma}{\sqrt n},
\qquad z=\frac{\bar x-\mu}{\sigma/\sqrt n}
\]

\[
\text{Approximate central 95% range for sample means}=\mu\pm1.96SE
\]

### 7. Hypothesis tests

Practise both types actually developed in the VK material:

- **Binomial tests:** Calculate the appropriate tail under the null probability.
- **One-sample z-tests:** Calculate SE, z, the correct tail probability, and the decision.

\[
z=\frac{\bar x-\mu_0}{\sigma/\sqrt n}
\]

Do the nine VK examples: quiz, coin, chip quality, server speed, battery life, spam filter, exam marks, cola preference and sensor calibration.

### 8. Encoding, BoW and n-grams

Build ordinal/one-hot/binary/frequency/target encoding tables. Construct a vocabulary and document-term matrix, and count contiguous n-grams.

\[
\text{Number of n-gram positions}=L-n+1
\]

Target encoding uses the target mean within each category.

### 9. Manual TF-IDF

Calculate TF, document frequency, IDF and the final matrix. JK’s worked example uses:

\[
TF=\frac{\text{term count}}{\text{document length}},
\quad IDF=\ln\left(\frac N{DF}\right),
\quad TFIDF=TF\times IDF
\]

Use the question’s convention; this differs from scikit-learn’s defaults.

### 10. Simple linear regression

Find coefficients, make predictions, calculate residuals and evaluate the fit.

\[
b_1=\frac{S_{xy}}{S_{xx}},
\qquad b_0=\bar y-b_1\bar x
\]

\[
SSE=\sum(y-\hat y)^2,\quad MSE=\frac{SSE}{n},\quad R^2=1-\frac{SSE}{SST}
\]

### 11. Multiple linear regression

Construct the design matrix, calculate XᵀX and Xᵀy, solve the normal equations, and predict for new features.

\[
X^\top Xb=X^\top y
\]

Practise the JK examples with both two and three input features.

### 12. Logistic regression

Calculate scores, sigmoid probabilities, classes, odds, cross-entropy, gradients and the first two parameter updates.

\[
p=\frac1{1+e^{-(b_0+b_1x)}},\qquad \text{odds}=\frac p{1-p}
\]

\[
L=-[y\ln p+(1-y)\ln(1-p)]
\]

For mean loss:

\[
g_0=\operatorname{mean}(p-y),\quad g_1=\operatorname{mean}((p-y)x),\quad b_j\leftarrow b_j-\eta g_j
\]

Also practise decision boundaries, accuracy, odds multipliers eᵇ¹, and the VK baseline-loss comparison.

### 13. K-means

Calculate distances, assign clusters, update means, repeat until stable, then calculate inertia.

\[
d^2=\sum_j(x_j-c_j)^2,\qquad J=\sum_i\|x_i-c_{\text{assigned}}\|^2
\]

### 14. SVM and kernel calculations

Solve support-vector equations, check constraints, find margin width and classify new points.

\[
f(x)=w^\top x+b,\quad y_if(x_i)\ge1,\quad \text{full margin width}=\frac2{\|w\|}
\]

Practise the VK worked example and substituting values into linear, polynomial, RBF and sigmoid kernel expressions.

### 15. SVR

Calculate predictions, absolute errors, epsilon losses, tube boundaries and objective values. Form the observation constraints.

\[
L_\varepsilon=\max(0,|y-f(x)|-\varepsilon)
\]

\[
J=\frac12\|w\|^2+C\sum L_\varepsilon
\]

### 16. PCA, if confirmed

Calculate column means, centered data, covariance matrix, eigenvalues/eigenvectors, component scores and explained variance.

\[
S=\frac{X_c^\top X_c}{n-1},\qquad Z=X_cW,\qquad EVR_j=\frac{\lambda_j}{\sum_k\lambda_k}
\]

## Scope distinctions and revision order

T-tests, chi-square tests and ANOVA are mentioned as examples, but the supplied testing lessons develop binomial and z-tests. KNN is a brief API example. PCA’s detailed faculty material remains pending.

For the current revision, start with statistics → distributions → CLT/tests → regression → K-means/SVM/SVR, then cover encoding calculations and programming output tracing.
