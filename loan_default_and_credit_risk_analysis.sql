USE loan_risk_analysis_clean;

-- How large is our loan portfolio, and how much money have we disbursed?
SELECT
    COUNT(*) AS total_loans,
    SUM(principal_amount_inr) AS total_disbursed,
    SUM(outstanding_balance_inr) AS total_outstanding
FROM loans;

-- Q2. Loan Distribution by Loan Type
SELECT
    loan_type,
    COUNT(*) AS total_loans,
    SUM(principal_amount_inr) AS total_disbursed
FROM loans
GROUP BY loan_type
ORDER BY total_loans DESC;

-- Q3. Overall Loan Default Rate
SELECT
    COUNT(*) AS total_loans,
    SUM(default_flag) AS defaulted_loans,
    ROUND(AVG(default_flag) * 100, 2) AS default_rate_pct
FROM loan_status;

-- Q4. Default Rate by Loan Type
SELECT
    l.loan_type,
    COUNT(*) AS total_loans,
    SUM(s.default_flag) AS defaulted_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN loan_status s
ON l.loan_id = s.loan_id
GROUP BY l.loan_type
ORDER BY default_rate_pct DESC;

-- Q5. Default Rate by Employment Type
SELECT
    c.employment_type,
    COUNT(*) AS total_loans,
    SUM(s.default_flag) AS defaulted_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY c.employment_type
ORDER BY default_rate_pct DESC;

-- Q6. Default Rate by Credit Score
SELECT
    CASE
        WHEN c.credit_score < 600 THEN 'Poor'
        WHEN c.credit_score < 700 THEN 'Average'
        WHEN c.credit_score < 750 THEN 'Good'
        ELSE 'Excellent'
    END AS credit_category,
    COUNT(*) AS total_loans,
    SUM(s.default_flag) AS defaulted_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY credit_category
ORDER BY default_rate_pct DESC;

-- Q7. Default Rate by Age Group
SELECT
    CASE
        WHEN c.age < 25 THEN 'Below 25'
        WHEN c.age <= 35 THEN '25-35'
        WHEN c.age <= 45 THEN '36-45'
        WHEN c.age <= 60 THEN '46-60'
        ELSE 'Above 60'
    END AS age_group,
    COUNT(*) AS total_loans,
    SUM(s.default_flag) AS defaulted_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY age_group
ORDER BY default_rate_pct DESC;

-- Q8. Default Rate by State
SELECT
    c.state,
    COUNT(*) AS total_loans,
    SUM(s.default_flag) AS defaulted_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY c.state
ORDER BY default_rate_pct DESC;

-- Q9. Repayment Performance
SELECT
    payment_status,
    COUNT(*) AS total_installments,
    SUM(amount_paid_inr) AS total_amount_collected
FROM repayments
GROUP BY payment_status
ORDER BY total_installments DESC;

-- Q10. Overdue Amount by DPD Bucket
SELECT
    dpd_bucket,
    COUNT(*) AS total_loans,
    SUM(overdue_amount_inr) AS total_overdue
FROM loan_status
GROUP BY dpd_bucket
ORDER BY total_overdue DESC;

-- Q11. Default Rate by Loan Amount
SELECT
    CASE
        WHEN l.principal_amount_inr < 100000 THEN 'Below 1 Lakh'
        WHEN l.principal_amount_inr < 500000 THEN '1-5 Lakhs'
        WHEN l.principal_amount_inr < 1000000 THEN '5-10 Lakhs'
        ELSE 'Above 10 Lakhs'
    END AS loan_range,
    COUNT(*) AS total_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY loan_range
ORDER BY default_rate_pct DESC;

-- Q12. Default Rate by Interest Rate
SELECT
    CASE
        WHEN annual_interest_rate_pct < 10 THEN 'Below 10%'
        WHEN annual_interest_rate_pct < 15 THEN '10-15%'
        WHEN annual_interest_rate_pct < 20 THEN '15-20%'
        ELSE 'Above 20%'
    END AS interest_range,
    COUNT(*) AS total_loans,
    ROUND(AVG(default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY interest_range
ORDER BY default_rate_pct DESC;

-- Q13. Default Rate by Loan Tenure
SELECT
    CASE
        WHEN tenure_months <= 12 THEN 'Up to 1 Year'
        WHEN tenure_months <= 36 THEN '1-3 Years'
        WHEN tenure_months <= 60 THEN '3-5 Years'
        ELSE 'Above 5 Years'
    END AS tenure_group,
    COUNT(*) AS total_loans,
    ROUND(AVG(default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY tenure_group
ORDER BY default_rate_pct DESC;

-- Q14. Recovery Performance by Loan Type
SELECT
    l.loan_type,
    COUNT(*) AS total_loans,
    SUM(s.overdue_amount_inr) AS total_overdue
FROM loans l
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY l.loan_type
ORDER BY total_overdue DESC;

-- Q15. Default Rate by City
SELECT
    c.city,
    COUNT(*) AS total_loans,
    SUM(s.default_flag) AS defaulted_loans,
    ROUND(AVG(s.default_flag) * 100, 2) AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN loan_status s ON l.loan_id = s.loan_id
GROUP BY c.city
ORDER BY default_rate_pct DESC;