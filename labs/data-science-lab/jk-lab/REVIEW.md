# IDSE lab question review

Reviewed the complete IDSE LAB.docx, including its two embedded question images and two data tables, all three standalone JPEG question sheets, and all seven CSV datasets. This is a review of the questions and data; no lab solution scripts or notebooks were present in idse_lab. Original files were left unchanged.

## Coverage

There are 19 question statements in total: 16 in the document and 3 in the separate photos. The photos overlap in their datasets and concepts but have distinct task lists.

| Source | Questions | Coverage |
| --- | ---: | --- |
| Lab 1 | 3 | Prime Number Analyzer, ATM Simulator, hard Number Guessing Game |
| Lab 2 | 1 | Student Performance Management System using five Python modules |
| Lab 3 | — | No heading or explicitly assigned questions found |
| Lab 4 | 3 | Student analysis, employee analysis, two-semester comparison |
| Lab 5 | 2 | Sales analysis, advanced employee analysis |
| Lab 6 | 2 | Cricket players, agricultural yields |
| Lab 7 | 2 | Steel strength outliers, server response percentiles |
| Lab 8 | 3 | Binomial defects, Poisson calls, geometric sales attempts |
| Lab 9 | 2 | Employee categorical encoding, shopping categorical encoding |
| Separate photos | 3 | Movie BoW, college-feedback TF-IDF, movie BoW versus TF-IDF |

The Prime Number Analyzer and ATM Simulator questions are images embedded under Lab 1, before the text-based number guessing question. They are easy to miss when extracting document text. The separate photos have no visible lab number, so they cannot confidently be assigned to Lab 3.

## Dataset checks

All seven datasets have consistent row widths, no empty cells, and no fully duplicated rows. These checks describe file integrity, not correctness of every recorded real-world measurement.

| File | Data rows | Used by |
| --- | ---: | --- |
| steel_rod_strength.csv | 60 | Lab 7 Q1 |
| server_response_times.csv | 80 | Lab 7 Q2 |
| items.csv | 30 | Lab 8 Q1; all days inspect 20 items |
| calls.csv | 9 frequency rows | Lab 8 Q2; frequencies sum to 60 intervals |
| customers.csv | 25 | Lab 8 Q3 |
| employee_encoding.csv | 15 | Lab 9 Q1 |
| customer_shopping.csv | 15 | Lab 9 Q2 |

Labs 4 and 5 explicitly ask students to construct their own DataFrames; no CSV is missing for those exercises. Both Lab 6 tables contain the stated 20 records inside the document.

## Requirements and points needing clarification

### Lab 1

- Prime analyzer: use a function and loops; validate integer input and reversed bounds. State whether range endpoints are inclusive. Handle ranges with no primes before requesting the largest prime; numbers below 2 are not prime.
- ATM: include balance, deposit, withdrawal, PIN change, a persistent menu, and lockout after three incorrect PIN attempts. Starting balance, initial PIN, new-PIN rules, and whether the attempt counter resets after login are unspecified. Reject nonpositive deposits and withdrawals as well as insufficient balances. Keep PINs as strings if leading zeros are allowed.
- Number guessing: the attempt limit, score formula, and meaning of “very close” are unspecified. State these choices explicitly. Decide whether invalid input consumes an attempt and keep that rule consistent.

### Lab 2

Use exactly the requested module structure: student.py, marks.py, attendance.py, report.py, and main.py. Cover add/search/report, five-subject marks and attendance, topper by GPA, eligibility lists, failed students, and invalid inputs.

Missing rules: grade thresholds, GPA scale and conversion, subject credits, subject pass mark, whether any subject failure means overall failure, tie handling for toppers, and semester validation. These must be declared as assumptions rather than presented as official policy. Overall attendance should use total attended classes divided by total conducted classes when subject class counts differ; a simple average of subject percentages can give a different answer. Handle zero conducted classes and duplicate roll numbers. Persistence across program restarts is not explicitly required.

### Lab 4

- Q1: construct exactly eight student records and cover head/tail, schema, statistics, filters, sorting, maximum marks, average marks, and department counts. Decide how to report ties for highest marks.
- Q2: construct at least ten employee records. Bonus is 10% for performance >= 8, otherwise 5%; apply the rule per employee. Include department salary means and counts, performance sorting, and maximum/minimum salaries.
- Q3: construct at least eight students in each semester, with overlap and missing marks/attendance. Fill each semester separately using its own mean and median before merging. Match on Student_ID, not row order. The question does not specify the merge type or which semester to use for department averages, highest department, or Result. A clear convention is an inner merge for comparable students and Semester 2 marks for final performance, with improvement = Semester 2 minus Semester 1. Keep this documented. Check that IDs are unique to prevent accidental many-to-many merges. Highest improvement may involve an imputed mark, which should be acknowledged in interpretation.

### Lab 5

- Q1: construct at least 12 sales records. The supplied formula treats Discount as a fixed currency amount per order, not a percentage. Sum sales across all orders for a product before selecting the highest-selling product. Sales bands must be Low < 5000, Medium >= 5000 and <= 10000, and High > 10000; a value of exactly 5000 must be Medium. Parse dates before extracting months. If records span years, group by year-month to avoid combining different years unintentionally.
- Q2: use at least 15 employees and add two exact duplicate records if the intent is to retain at least 15 unique employees after deduplication. The prompt is not explicit about the minimum after cleaning. Remove duplicates before aggregates and rankings. Experience bands assume integer years; fractional experience between 2 and 3 requires an explicit convention. Performance bands are >= 9 Excellent, >= 7 and < 9 Good, and < 7 Needs Improvement. Specify ranking tie behavior and report up to two top performers for departments with fewer than two employees. “Department and then Salary in descending order” could mean both descending; state the chosen order.

### Lab 6

- Q1: use all 20 supplied cricket records. Match the stated thresholds even though they make most players Excellent. Use runs as the primary descending sort key and strike rate as the secondary key. Include empty Team × Role cells as zero in the count pivot. Highest wicket-taker and top two run scorers are separate within-team calculations.
- Q2: use all 20 supplied farm records. The combined rainfall/fertilizer/yield condition uses AND. Exactly 1000 and 2000 belong to Medium. The dataset has no Low-yield farms, so show Low = 0 rather than treating the missing category as a data error. Yield units and whether Yield is per farm or per acre are unspecified; do not silently divide by Area_Acres. Calculate the requested fertilizer efficiency as Yield / Fertilizer_Used; no zero fertilizer values occur in the supplied data.

### Lab 7

- Q1: distinguish global IQR fences from separately calculated batch fences. The question asks about outliers in tensile strength and elongation, then says to remove “the outliers” without specifying whether to remove tensile outliers only or the union of both sets. Report the chosen rule and resulting row count. Compare sample standard deviations consistently. Flagging an observation statistically does not establish that it is a measurement error; engineering context is needed before deletion.
- Q2: use linear-interpolated quantiles consistently with Pandas defaults. “Percentile rank” has multiple conventions; define it, for example percentage of observations <= 150 ms. Determine SLA compliance directly by counting requests <= 220 ms. Speed categories are Fast < Q1, Normal Q1 through Q3 inclusive, and Slow > Q3. Compare server consistency using within-server IQR, with server sample counts alongside the results.

### Lab 8

- Q1: estimate defect probability as mean daily defects / 20. Compute P(X >= 4) as 1 - P(X <= 3). The model needs independent trials and a stable probability as well as binary outcomes; binary outcomes alone do not establish a binomial model. The data offer a descriptive comparison, not proof of those assumptions or of the factory guarantee.
- Q2: calls.csv is an aggregated frequency table, not 60 raw interval rows. Use frequency-weighted calculations or expand the counts. P(overwhelmed) = P(X > 5) = P(X >= 6). Include the Poisson tail beyond k = 8 if an expected-frequency table is intended to total exactly 60. A staffing recommendation also needs an acceptable overload rate, service time, staffing capacity, and cost information; state these limits.
- Q3: X counts customers through the first successful sale, starting at 1. Estimate p as 1 / sample mean. Use P(X > 3) = (1 - p)^3. Seed the simulation for reproducibility, and expect its mean to differ slightly from the observed mean. The sample mean does not meet the “fewer than 2” target, but a formal population-level claim requires further inference.
- All three: specify sample variance (denominator n - 1) or population variance (denominator n); both are defensible for different purposes and yield different numbers here.

### Lab 9

- Q1: preserve an original copy for comparison. Explicitly specify both ordinal orders. Work_Mode is nominal, so the requested label encoding creates arbitrary numeric codes; explain that limitation. One-hot Department with all four indicator columns increases the original six-column table to nine columns when replacing Department; adding its separate frequency feature makes ten columns. Keeping the original Department too changes those counts. State whether frequency encoding uses counts or proportions.
- Q2: Membership must map to 1, 2, 3 exactly. Product_Category has four categories. Delivery_Mode label codes are arbitrary. Payment_Method frequency values can be counts or proportions, but the convention must be stated. Use the requested encoding library for Customer_ID binary encoding, then retain the encoded identifier separately from predictive features. With 15 unique identifiers, a typical 1-based binary category mapping needs four bits; exact output and unknown-category handling depend on encoder settings. IDs do not become informative predictors simply because they are encoded. Save both requested output CSV filenames when implementing.

### Separate photo exercises

- Movie BoW: lowercase, vocabulary, count matrix, five most frequent tokens, overlap of reviews 1 and 3, and repeat with English stop words removed.
- College TF-IDF: lowercase, vocabulary and matrix, three highest-weight words in feedback 1, repeated-word interpretation, and repeat with max_features = 5.
- Movie BoW versus TF-IDF: display both vocabularies and matrices, compare “excellent” across all five reviews, compare another repeated word, and give three observations.
- Use consistent preprocessing for fair comparisons. Default TF-IDF includes smoothed inverse document frequency and L2 row normalization; different weights can reflect both word rarity and document composition. It does not automatically remove stop words or stem words. For feedback max_features = 5, the fifth slot has a corpus-frequency tie between are, excellent, and facilities; explain tie behavior rather than inventing a semantic priority.

## Verified numerical checkpoints

Computed from the supplied CSVs with Python standard-library arithmetic. Quantiles below use linear interpolation at position (n - 1) × p. Standard deviations and sample variances use denominator n - 1. These are checkpoints, not complete solutions or generated plots.

### Lab 6 tables

- Cricket top five by runs: Virat 5800, Warner 5700, Rohit 5600, Root 5500, Smith 5400.
- Roles: Batsman 8, All-Rounder 3, Bowler 5, Wicketkeeper 4.
- Performance: Excellent 15, Good 1, Average 4.
- Farm average yield: 2290. Crop averages: Cotton 1687.5, Maize 1900, Rice 2540, Sugarcane 3900, Wheat 1762.5.
- Highest average crop yield: Sugarcane. Yield categories: Low 0, Medium 9, High 11.

### Lab 7

- Steel tensile Q1 = 502.025, Q3 = 532.8, IQR = 30.775; fences 455.8625 and 578.9625 MPa.
- Tensile outliers: S008 = 410.0 (Batch_A), S027 = 615.5 (Batch_B), S049 = 398.2 (Batch_C). All three batches contain one tensile outlier.
- Highest batch median: Batch_C = 536.85 MPa; Batch_A = 511.8 and Batch_B = 501.85.
- Elongation Q1 = 16.8, Q3 = 18.5, IQR = 1.7; fences 14.25 and 21.05. One outlier: S034 = 26.8, Batch_B.
- Removing only the three tensile outliers leaves 57 rows. Tensile mean changes from 514.9867 to 517.1140; sample standard deviation from 32.3525 to 21.8486. The standard deviation changes more in both absolute and relative terms. Removing the union with the elongation outlier would leave 56 rows and different summaries.
- Server mean = 134.23375 ms; median = 119.05 ms. The larger mean is consistent with the long upper tail.
- Server percentiles: P10 = 79.61, P25 = 98.125, P50 = 119.05, P75 = 156.4, P90 = 195.63, P95 = 216.345 ms.
- Server IQR = 58.275 ms; range = 437.7 ms; fences 10.7125 and 243.8125 ms. Outliers: R013 = 480.0 and R056 = 455.5 ms.
- SLA: 76 / 80 = 95% at or below 220 ms, so the observed dataset meets the target exactly.
- Percentile rank at 150 ms using <=: 73.75%.
- Server IQRs: Server_1 39.2, Server_2 32.05, Server_3 67.7, Server_4 55.8 ms. Server_2 is most consistent by IQR.
- Speed counts: Fast 20, Normal 40, Slow 20.

### Lab 8

| Model | Verified checkpoints |
| --- | --- |
| Binomial | Daily mean 1.966667; sample variance 1.412644; population variance 1.365556; estimated p = 0.0983333 |
| Binomial probabilities | P(0) = 0.126160; P(2) = 0.285091; P(X >= 4) = 0.127029 |
| Zero-defect days at p = 0.10 | Expected 3.6473 out of 30; observed 3 |
| Poisson | 60 intervals; lambda = 2.866667; sample variance 2.524294; population variance 2.482222 |
| Poisson probabilities | P(0) = 0.056888; P(3) = 0.223359; P(X >= 6) = 0.071077 |
| Overload | Model estimate 7.1077%; observed 4 / 60 = 6.6667% |
| Poisson tail beyond 8 | Expected 0.170211 intervals; include a tail row when totaling expected frequencies |
| Geometric | Mean 2.64; estimated p = 0.378788 |
| Geometric probabilities | P(1) = 0.378788; P(3) = 0.146176; P(X > 3) = 0.239729 |
| First-customer sale | Expected 9.4697 out of 25; observed 10 |

### Lab 9 and photo exercises

- Employee department counts: IT 4, HR 4, Sales 4, Finance 3. All work modes occur five times.
- Shopping payment counts: Credit Card 5, UPI 6, Cash 4. Membership counts: Gold 6, Silver 5, Bronze 4. Product category counts: Electronics 4, Clothing 4, Groceries 3, Books 4.
- Movie vocabulary without stop-word filtering: 12 tokens. Five most frequent: and 4, excellent 4, story 3, the 3, was 3; ordering within ties can vary.
- Words common to movie reviews 1 and 3: and, excellent.
- “excellent” BoW values: [1, 0, 2, 0, 1]. Corresponding TF-IDF values with default smoothed IDF and L2 normalization: approximately [0.388949, 0, 0.747490, 0, 0.374447]. These were independently calculated from the standard formula, not executed through scikit-learn.
- Feedback vocabulary: 19 tokens. First-feedback highest-weight words: clearly, concepts, explain, tied at approximately 0.510893 each under those TF-IDF settings.

## Review limits

No implementations, plots, simulations, or encoded output files were present to test. No files were rewritten. This review validates the provided question content, dataset structure, and selected numerical outputs; it does not certify a completed lab submission.
