# IDSE Course Topics Through Logistic Regression
## Introduction to Data Science for Engineers
**Study scope:** Python, data analysis, statistical inference, preprocessing, and machine learning through logistic regression.

**Source:** The supplied reconstructed syllabus, cross-checked against the lab questions already reviewed. The lab checkpoints below identify practical requirements. Confirm theory-only topics and specific exam requirements against faculty materials.

## Study progress and to-do

- [x] **Unit 1 covered:** Python and modules, NumPy, Pandas and data cleaning, EDA, descriptive statistics, Matplotlib, and Seaborn.
- [x] **Unit 2 covered:** Probability rules and Bayes’ theorem, random variables, distributions and SciPy, sampling, standard error, the Central Limit Theorem, confidence intervals, and hypothesis testing fundamentals.
- [ ] **Next — Unit 3:** Categorical encoding, feature engineering, Bag of Words, TF-IDF, and the scikit-learn workflow.
- [ ] **Then — Unit 4:** Machine learning fundamentals, linear regression, and logistic regression.
- [ ] **Independent practice:** Write the full Lab 2 program, complete an EDA exercise, and solve the binomial, Poisson, and geometric labs. Confirm which named hypothesis tests are required.

Checked items mean we covered the topics together. Independent coding practice is tracked separately.

---

# UNIT 1 — Python Programming and Data Analysis

## 1. Python Fundamentals
- Introduction to Python and its applications in Data Science
- Variables and data types
- Type conversion and type checking
- Operators: arithmetic, comparison, logical, assignment and membership
- Input and output operations
- Conditional statements: `if`, `elif`, `else`
- Loops: `for` and `while`
- Loop control: `break`, `continue`, `pass`
- Strings and string manipulation
- Lists and list operations
- Tuples
- Sets and set operations
- Dictionaries and dictionary operations
- List, dictionary and set comprehensions
- Functions and function arguments
- Default and keyword arguments
- Lambda functions
- Built-in functions
- Exception handling: `try`, `except`, `else`, `finally`
- Modules and packages
- Importing modules and using libraries

## 2. NumPy — Numerical Computing
- Introduction to NumPy
- Creating NumPy arrays
- Array attributes: `ndim`, `shape`, `size`, `dtype`
- Array creation methods: `array()`, `zeros()`, `ones()`, `arange()`, `linspace()`, `random`
- Indexing and slicing
- Reshaping arrays
- Flattening and transposing arrays
- Array concatenation and splitting
- Mathematical and arithmetic operations
- Element-wise operations
- Broadcasting
- Vectorization
- Boolean indexing and filtering
- Sorting and searching
- Aggregation functions: `sum()`, `mean()`, `min()`, `max()`, `std()`, `var()`
- Axis-based operations
- Matrix operations
- Dot product and matrix multiplication
- Random number generation

## 3. Pandas — Data Manipulation and Cleaning

### 3.1 Pandas Fundamentals
- Introduction to Pandas
- Series and DataFrames
- Creating Series and DataFrames
- Reading CSV files using `read_csv()`
- Understanding datasets: `head()`, `tail()`, `shape`, `columns`, `dtypes`
- Dataset inspection using `info()` and `describe()`
- Selecting columns and rows
- Indexing using `loc[]` and `iloc[]`
- Filtering rows using conditions
- Sorting using `sort_values()`, counting with `value_counts()` and `nunique()`, and selecting top rows with `nlargest()`
- Ranking with `rank()` and grouping numeric ranges with `pd.cut()`
- Adding and removing columns
- Renaming columns
- Updating values
- Applying functions using `apply()` and `map()`

### 3.2 Advanced Pandas and Data Cleaning
- Handling missing values
- Detecting missing values using `isnull()` and `notnull()`
- Removing missing values using `dropna()`
- Filling missing values using `fillna()`
- Detecting and removing duplicates
- Type conversion using `astype()`, `pd.to_numeric()`, and `pd.to_datetime()`
- Check impossible values and inconsistent categories before filling missing data
- String operations using `.str`
- Date and time operations
- Grouping using `groupby()`
- Aggregation using `agg()`
- Multiple aggregations
- Applying custom functions
- Combining DataFrames
- Concatenation using `concat()`
- Merging and joining using `merge()`
- Pivot tables using `pivot_table()`
- Crosstabulation using `crosstab()`
- Resetting and setting indexes
- Exporting processed data to CSV

## 4. Exploratory Data Analysis (EDA) and Data Visualization

### 4.1 EDA Fundamentals
- Introduction to Exploratory Data Analysis
- Objectives and importance of EDA
- Understanding dataset structure
- Identifying numerical and categorical variables
- Data quality assessment
- Identifying missing values and duplicates
- Univariate, bivariate and multivariate analysis

### 4.2 Matplotlib
- Introduction to Matplotlib
- Figure and axes
- Titles, labels and legends
- Customizing plots
- Line plots
- Bar charts and horizontal bar charts
- Scatter plots
- Histograms
- Boxplots
- Subplots
- Grid, markers and plot styling
- Saving visualizations

### 4.3 Seaborn
- Introduction to Seaborn
- Distribution plots and histograms
- KDE plots
- Boxplots
- Violin plots
- Scatterplots
- Line plots
- Barplots
- Countplots
- Pairplots
- Heatmaps
- Correlation heatmaps
- Group-wise visualization

### 4.4 Descriptive Statistics
- Measures of central tendency:
  - Mean
  - Median
  - Mode
- Measures of dispersion:
  - Range
  - Variance
  - Standard deviation
  - Interquartile range (IQR)
- Quartiles: Q1, Q2 and Q3
- Percentiles
- Minimum, maximum and five-number summary
- Outlier detection using the IQR method
- Z-score method for outlier detection
- Distribution shapes
- Skewness: positive, negative and symmetric
- Kurtosis
- Covariance
- Correlation and Pearson correlation coefficient
- Interpreting statistical summaries and visualizations

---

# UNIT 2 — Probability, Distributions and Statistical Inference

## 5. Probability Fundamentals
- Introduction to probability
- Experiments, sample spaces and events
- Types of events
- Basic probability rules
- Addition and multiplication rules
- Complementary events
- Conditional probability
- Independent and dependent events
- Bayes' theorem
- Random variables
- Discrete and continuous random variables
- Probability mass functions (PMF)
- Probability density functions (PDF)
- Cumulative distribution functions (CDF)
- Expected value and variance of random variables

## 6. Probability Distributions

### 6.1 Bernoulli Distribution
- Definition and characteristics
- Success and failure outcomes
- Probability mass function
- Mean and variance
- Python implementation and simulation

### 6.2 Binomial Distribution
- Definition and assumptions
- Fixed number of independent trials
- Number of successes
- Probability mass function
- Mean and variance
- Calculating exact and cumulative probabilities
- Expected versus observed frequencies
- Python implementation using SciPy

### 6.3 Poisson Distribution
- Definition and characteristics
- Event counts in a fixed interval
- Rate parameter (lambda)
- Probability mass function
- Mean and variance
- Probability calculations
- Python implementation and simulation

### 6.4 Geometric Distribution
- Number of trials until the first success
- Probability mass function
- Mean and variance
- Probability calculations
- Python implementation

### 6.5 Normal Distribution
- Introduction to the normal distribution
- Bell-shaped curve
- Mean and standard deviation
- Standard normal distribution
- Z-score
- Empirical rule (68–95–99.7)
- Probability calculations using CDF
- PDF and CDF visualization
- Python implementation using SciPy

### 6.6 Distribution Comparison and Simulation
- Comparing discrete and continuous distributions
- Choosing an appropriate probability distribution
- Random sampling
- Generating simulated observations
- Theoretical versus empirical probabilities
- Expected versus observed frequencies
- Visualizing distributions

### 6.7 Python and SciPy for Probability
- `scipy.stats`
- `pmf()` and `pdf()`
- `cdf()` and `sf()`
- `ppf()`
- `rvs()`
- Distribution parameters
- Calculating probabilities using Python
- Plotting probability distributions

## 7. Sampling and Hypothesis Testing

### 7.1 Statistical Inference
- Population and sample
- Parameters and statistics
- Sampling methods
- Sampling distributions
- Sampling variability
- Standard error
- Introduction to the Central Limit Theorem

### 7.2 Hypothesis Testing
- Introduction to hypothesis testing
- Null hypothesis (H0)
- Alternative hypothesis (H1)
- Significance level (alpha)
- Test statistic
- P-value and its interpretation under the null hypothesis
- One-sided and two-sided alternatives
- Critical value
- Type I and Type II errors
- Confidence intervals
- Rejecting or failing to reject the null hypothesis
- Interpreting statistical test results

**Note:** Specific tests such as Z-tests, t-tests, chi-square tests and ANOVA should be included in the confirmed syllabus only after checking the lecture material.

---

# UNIT 3 — Data Preprocessing and Feature Engineering

## 8. Feature Encoding and Data Transformation

### 8.1 Categorical Data
- Numerical and categorical features
- Nominal and ordinal variables
- Encoding categorical variables
- Label encoding
- Ordinal encoding
- One-hot encoding
- Binary encoding
- Frequency encoding
- Choosing an appropriate encoding technique

### 8.2 Feature Engineering
- Introduction to feature engineering
- Feature creation and transformation
- Handling categorical variables
- Feature selection fundamentals
- Preparing data for machine learning
- Data leakage: split first, fit preprocessing on training data, and reuse it on test data
- Feature scaling as a preparation concept for gradient-based models

## 9. Text Processing and Feature Extraction

### 9.1 Natural Language Processing Fundamentals
- Introduction to text data
- Text preprocessing
- Tokenization
- Lowercase conversion
- Removing punctuation
- Stop-word removal
- Basic text normalization

### 9.2 Bag of Words (BoW)
- Introduction to Bag of Words
- Vocabulary construction
- Document-term matrix
- Word frequency
- CountVectorizer
- Transforming text into numerical features

### 9.3 TF-IDF
- Term Frequency (TF)
- Inverse Document Frequency (IDF)
- TF-IDF calculation
- TF-IDF vectorization
- TfidfVectorizer
- Comparing Bag of Words and TF-IDF
- Limiting vocabulary with `max_features` and reading the resulting feature names
- Feature representation of text documents

## 10. Scikit-learn Fundamentals

- Introduction to Scikit-learn
- Machine learning workflow
- Features (X) and target (y)
- Numerical and categorical feature preparation
- `fit()`
- `transform()`
- `fit_transform()`
- `predict()`
- Data preprocessing with Scikit-learn
- Model training and prediction
- Basic model evaluation
- Train-test splitting using `train_test_split()` 

---

# UNIT 4 — Machine Learning and Regression

## 11. Introduction to Machine Learning

### 11.1 ML Fundamentals
- Introduction to Machine Learning
- Applications of Machine Learning
- Traditional programming versus Machine Learning
- Supervised learning
- Unsupervised learning
- Classification and regression
- Features and target variables
- Training and testing data
- Model training and prediction
- Generalization
- Overfitting and underfitting
- Basic model evaluation

### 11.2 Regression Fundamentals
- Introduction to regression
- Independent and dependent variables
- Relationship between variables
- Prediction of continuous values
- Regression line
- Actual and predicted values
- Residuals
- Model coefficients and intercept

## 12. Linear Regression

### 12.1 Simple Linear Regression
- Introduction to Linear Regression
- Mathematical equation of a straight line
- Simple linear regression equation
- Slope and intercept
- Relationship between input and output
- Least squares method
- Best-fit regression line
- Actual versus predicted values
- Residual calculation
- Sum of Squared Errors

### 12.2 Multiple Linear Regression
- Introduction to Multiple Linear Regression
- Multiple independent variables
- Regression equation with multiple features
- Coefficients and intercept
- Matrix representation
- Model fitting
- Prediction using multiple features
- Interpretation of coefficients
- Residual analysis

### 12.3 Model Evaluation
- Mean Squared Error (MSE)
- Residuals
- Actual versus predicted comparison
- Evaluating prediction performance
- Interpreting prediction error and the units of MSE

### 12.4 Python Implementation
- Least squares with NumPy using an intercept column and `np.linalg.lstsq()`
- Linear regression using scikit-learn for the general workflow. The delivery-time lab requires NumPy/Python coefficients.
- Training a regression model
- Making predictions
- Extracting coefficients and intercept
- Calculating MSE
- Plotting regression lines
- Evaluating multiple linear regression

## 13. Logistic Regression

### 13.1 Classification Fundamentals
- Introduction to classification
- Classification versus regression
- Binary classification
- Positive and negative classes
- Features and binary target variables
- Predicted probabilities
- Classification thresholds

### 13.2 Logistic Regression Mathematics
- Introduction to Logistic Regression
- Linear combination of input features
- Sigmoid function
- Converting linear output into probabilities
- Probability interpretation
- Decision boundary
- Classification threshold (commonly 0.5)
- Binary class prediction

### 13.3 Logistic Regression Optimization
- Model parameters: weights and bias
- Cost function
- Binary cross-entropy / log loss
- Gradient descent
- Learning rate
- Weight and bias updates
- Iterations and convergence
- Model training from scratch

### 13.4 Logistic Regression Evaluation
- Predicted probabilities
- Converting probabilities into class labels
- Accuracy
- Classification errors
- Basic classification evaluation. The lab requires manual accuracy. Confirm confusion matrices, precision, and recall against lecture materials.

### 13.5 Python Implementation
- Implementing Logistic Regression from scratch using NumPy
- Initializing weights and bias
- Implementing the sigmoid function
- Calculating predicted probabilities
- Computing binary cross-entropy loss
- Calculating gradients
- Updating parameters using gradient descent
- Training the model
- Making predictions
- Calculating classification accuracy
- Comparing predictions with actual labels

---

# Practical / Laboratory Component

Use the lab exercises to practice the theory in each unit.

| Area | Practical skills |
|---|---|
| Python | Programming exercises, functions, collections and modules |
| NumPy | Array operations and numerical calculations |
| Pandas | Dataset loading, cleaning and manipulation |
| EDA | Statistical summaries and visualizations |
| Statistical analysis | Percentiles, quartiles, IQR and outliers |
| Probability | Distribution calculations and simulations |
| Statistical inference | Sampling and probability-based analysis, where included |
| Encoding | Transforming categorical variables |
| NLP | Bag of Words and TF-IDF |
| Linear Regression | Training, prediction and MSE |
| Logistic Regression | Implementation from scratch and accuracy |

## Important Lab 7 datasets

**1. `steel_rod_strength.csv`**
- Dataset inspection
- Overall tensile-strength boxplot
- IQR-based outlier detection
- Production batch comparisons
- Elongation analysis
- Removing outliers
- Comparing mean and standard deviation before and after cleaning

**2. `server_response_times.csv`**
- Mean and median
- Percentile calculations
- Range and IQR
- Outlier detection
- SLA compliance
- Percentile rank
- Server-wise comparison
- Fast, normal and slow response categories
- Histogram visualization

## Regression lab checkpoints

- **Delivery time:** Fit multiple linear regression from distance and item count. Predict for 10 km and 6 items, calculate MSE, and plot actual versus predicted times.
- **Eye strain:** Fit logistic regression from scratch. Use zero initial coefficients, learning rate 0.1, and 8,000 iterations. Predict at 5.5 hours, classify at a 0.5 threshold, compute accuracy manually, and plot probabilities.

## Other laboratory areas
- Python modules and programming exercises
- Data manipulation and statistical analysis
- Probability distribution exercises using `items.csv`, `calls.csv` and `customers.csv`
- Categorical encoding
- Bag of Words and TF-IDF
- Regression and classification implementations

---

# Important Python Libraries to Master

| Library | Main purpose |
|---|---|
| Python standard library | General programming and modules |
| NumPy | Numerical computing |
| Pandas | Data manipulation |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| SciPy | Statistical functions and distributions |
| Scikit-learn | Preprocessing and ML |
| NLTK / text utilities | Text preprocessing, if used in the practical |

---

# Final Scope

The learning sequence is:

**Python → NumPy → Pandas → EDA → Descriptive Statistics → Probability → Statistical Inference → Feature Encoding → NLP Feature Extraction → Scikit-learn → Linear Regression → Logistic Regression.**

This syllabus is a reconstructed study syllabus based on the IDSE topics and lab work discussed, not a verbatim official faculty syllabus. In particular, specific hypothesis tests, additional ML algorithms, and optional evaluation techniques must be verified against your lecture notes before treating them as exam requirements.
