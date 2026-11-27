# IDSE lab portions through logistic regression

**Progress:** 23 of 23 complete, 0 remaining.

This index maps all 24 screenshots in this folder to 23 question prompts. The student management question spans two screenshots. 

The [original question sheet](../IDSE%20LAB.docx) confirms Labs 1, 2, and 4–9. The screenshots appear in reverse teaching order. Text encoding follows categorical encoding, which makes Lab 10 its likely placement. Both regression exercises appear after text encoding in that sequence, but their screenshots have no visible lab labels. The exact numbering and whether the regression exercises share one lab remain unconfirmed. Lab 3 has no identifiable prompt in either source.

The seven CSVs are in the [parent lab folder](../). The cricket, farm, and regression tables are inside their respective screenshots. Labs 4 and 5 ask you to create the datasets yourself.

## Lab 1 — Python functions and exceptions

- [x] **Prime Number Analyzer.** Read an inclusive range, find primes with loops and a function, display the count and largest prime, and handle invalid input and reversed ranges. [Screenshot 26](WhatsApp%20Image%202026-11-09%20at%2019.39.26.jpeg)
- [x] **ATM Simulator.** Check balance, deposit, withdraw, and change PIN. Limit incorrect PIN attempts to three, reject overdrafts, handle nonnumeric input, and loop until Exit. [Screenshot 25 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.25%20%281%29.jpeg)
- [x] **Number Guessing Game.** Choose a random integer from 1 to 1000, limit guesses, give high/low/very-close hints, and use functions for generation, validation, and scoring. [Screenshot 25](WhatsApp%20Image%202026-11-09%20at%2019.39.25.jpeg)

## Lab 2 — Student Performance Management System

- [x] **Student system.** Use student.py, marks.py, attendance.py, report.py, and main.py. Record student details and five subjects, compute total, average, grade, GPA, and attendance, apply the 75% eligibility rule, print reports, search by roll number, find the topper, and list eligible, ineligible, and failed students. Both screenshots form one question. [Screenshot 24 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.24%20%281%29.jpeg) · [Screenshot 24](WhatsApp%20Image%202026-11-09%20at%2019.39.24.jpeg)

## Lab 3 — Missing from the supplied material

The numbered sheet jumps from Lab 2 to Lab 4. No separate Lab 3 question was identifiable in the screenshot sequence.


## Lab 4 — Pandas DataFrames

- [x] **Student dataset.** Create eight records. Use head, tail, dtypes, describe, mean, highest marks, marks > 75, descending sort, and department counts. [Screenshot 23](WhatsApp%20Image%202026-11-09%20at%2019.39.23.jpeg)
- [x] **Employee dataset.** Create at least ten records. Filter IT and salary above ₹50,000, summarize salary and department counts, sort performance, and calculate 10% bonus for scores ≥ 8 and 5% otherwise. [Screenshot 22 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.22%20%281%29.jpeg)
- [x] **Two-semester comparison.** Create at least eight records per semester with overlapping students. Fill missing marks with the semester mean and attendance with the semester median. Merge on Student_ID, calculate improvement, identify improvements > 10, summarize departments, and assign result bands at 60 and 85. [Screenshot 22](WhatsApp%20Image%202026-11-09%20at%2019.39.22.jpeg)

## Lab 5 — Sales and advanced employee analysis

- [x] **Company sales.** Create at least 12 orders. Practice loc, iloc, query, groupby, nunique, sales bands, dates, and pivot tables. Total sales = quantity × unit price − discount. Summarize by category, region, product, and month. [Screenshot 21 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.21%20%281%29.jpeg)
- [x] **Employee performance.** Create at least 15 employee records and include duplicates. Detect and remove duplicates, rename columns, filter by salary and performance, aggregate departments, rank salaries, classify experience/performance, select top employees, pivot average salary, and group by joining year. [Screenshot 21](WhatsApp%20Image%202026-11-09%20at%2019.39.21.jpeg)

## Lab 6 — Cricket and farm analysis

- [x] **Cricket players.** Use the supplied 20-player table. Filter runs and wickets, find top players overall and by team, summarize team and role, assign performance categories, rank runs, and make a Team × Role count pivot. [Screenshot 20](WhatsApp%20Image%202026-11-09%20at%2019.39.20.jpeg)
- [x] **Farm yields.** Use the supplied 20-farm table. Filter rainfall, fertilizer, and yield, summarize yield by crop and soil, categorize and rank yields, compute yield ÷ fertilizer used, and make a Crop × Season average-yield pivot. [Screenshot 19 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.19%20%281%29.jpeg)

## Lab 7 — Outliers and percentiles

- [x] **Steel rods.** Use steel_rod_strength.csv. Make overall and batch boxplots, calculate quartiles, IQR, and 1.5 × IQR fences for tensile strength and elongation, identify outliers, compare mean and standard deviation before/after removal, and discuss whether to investigate the readings. [Screenshot 19](WhatsApp%20Image%202026-11-09%20at%2019.39.19.jpeg)
- [x] **Server response times.** Use server_response_times.csv. Compare mean and median, calculate percentiles, range, IQR, and fences, find the percentile rank of 150 ms, check the 95% within 220 ms SLA, compare servers by IQR, classify speed, and plot a histogram with quartile lines. [Screenshot 18 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.18%20%281%29.jpeg)

## Lab 8 — Discrete probability distributions

- [x] **Binomial defects.** Use items.csv. Find mean and variance, estimate p = mean ÷ 20, compute P(X = 0), P(X = 2), and P(X ≥ 4), plot theoretical PMF against observed relative frequency, and compare expected and actual zero-defect days at p = 0.10. [Screenshot 18](WhatsApp%20Image%202026-11-09%20at%2019.39.18.jpeg)
- [x] **Poisson help-desk calls.** Use the frequency table in calls.csv. Check 60 intervals, calculate weighted mean λ and variance, compute P(X = 0), P(X = 3), and P(X ≥ 6), compare observed and expected frequency plots, and discuss staffing based on overload risk. [Screenshot 17](WhatsApp%20Image%202026-11-09%20at%2019.39.17.jpeg)
- [x] **Geometric first sale.** Use customers.csv. Build a histogram/frequency table, estimate p = 1 ÷ mean, compute P(X = 1), P(X = 3), and P(X > 3), compare first-customer sales, simulate 1,000 days, and assess the target of fewer than two attempts on average. [Screenshot 16 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.16%20%281%29.jpeg)

## Lab 9 — Categorical encoding

- [x] **Employee encoding.** Use employee_encoding.csv. Label-encode Work_Mode, ordinal-encode Performance and Education in the given orders, one-hot-encode Department, add Department frequencies, compare widths, and save employee_encoding_output.csv. [Screenshot 16](WhatsApp%20Image%202026-11-09%20at%2019.39.16.jpeg)
- [x] **Shopping encoding.** Use customer_shopping.csv. Ordinal-encode Membership (Bronze 1, Silver 2, Gold 3), one-hot-encode Product_Category, label-encode Delivery_Mode, frequency-encode Payment_Method, and binary-encode Customer_ID separately. Compare widths and save customer_shopping_encoded.csv. [Screenshot 15 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.15%20%281%29.jpeg)

## Text encoding — Likely Lab 10

- [x] **Movie reviews with Bag of Words.** Lowercase the reviews, use CountVectorizer, show the vocabulary and document-term matrix, find the five most frequent words and the overlap of reviews 1 and 3, and rerun with English stop words removed. [Screenshot 15](WhatsApp%20Image%202026-11-09%20at%2019.39.15.jpeg)
- [x] **College feedback with TF-IDF.** Use TfidfVectorizer on the lowercased feedback, show the vocabulary and matrix, identify the three highest-weight words in the first sentence, interpret common words, and compare with max_features=5. [Screenshot 14 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.14%20%281%29.jpeg)
- [x] **Movie reviews comparing BoW and TF-IDF.** Show both matrices and vocabularies for the same reviews, compare “excellent” and another repeated word, and write three observations. These three text questions also appear in the separate November 7 photos. [Screenshot 14](WhatsApp%20Image%202026-11-09%20at%2019.39.14.jpeg)

## Multiple linear regression — Lab number unconfirmed

- [x] **Predict delivery time.** Use the ten supplied orders. Fit Y = β₀ + β₁ × distance + β₂ × item count using least squares in Python/NumPy. Calculate the coefficients without sklearn LinearRegression. Predict the delivery time for 10 km and 6 items, calculate MSE, display actual and fitted times, and plot the comparison. [Screenshot 13 (1)](WhatsApp%20Image%202026-11-09%20at%2019.39.13%20%281%29.jpeg)

## Logistic regression — Lab number unconfirmed

- [x] **Predict eye strain.** Use the ten supplied screen-time observations (0–9 hours). Start β₀ = β₁ = 0 with learning rate 0.1 and 8,000 iterations. Compute sigmoid probabilities and use averaged gradients to update both coefficients. Report the fitted coefficients and the probability at 5.5 hours, classify at a 0.5 threshold, calculate accuracy manually, display each actual class/probability/prediction, and plot predicted probabilities with the threshold line. [Screenshot 13](WhatsApp%20Image%202026-11-09%20at%2019.39.13.jpeg)
