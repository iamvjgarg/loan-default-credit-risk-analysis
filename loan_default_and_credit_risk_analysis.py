import pandas as pd
import numpy as np
from pathlib import Path

folder = Path(__file__).parent

customers = pd.read_csv(folder / "Customers.csv")
loans = pd.read_csv(folder / "Loans.csv")
repayments = pd.read_csv(folder / "Repayments.csv")
loan_status = pd.read_csv(folder / "Loan_Status.csv")

print("All datasets loaded successfully!")

# Overall Loan Portfolio
print("Total Loans:", len(loans))

print("Total Disbursed: ₹", loans["principal_amount_inr"].sum())

print("Total Outstanding: ₹", loans["outstanding_balance_inr"].sum())

# Which loan types contribute the most to the bank's portfolio?
print(
    loans.groupby("loan_type")["loan_id"]
    .count()
    .sort_values(ascending=False)
)

# What percentage of the bank's loans have defaulted?
print("Total Loans:", len(loan_status))

print("Defaulted Loans:", loan_status["default_flag"].sum())

print("Default Rate:", round(loan_status["default_flag"].mean() * 100, 2), "%")

# Which loan types have the highest default rates?
data = loans.merge(loan_status, on="loan_id")

print(
    data.groupby("loan_type")["default_flag"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False)
)

# Which employment categories have the highest loan default rates?
data = data.merge(customers, on="customer_id")

print(
    data.groupby("employment_type")["default_flag"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False)
)

# Which credit score category has the highest default rate?
data["credit_category"] = pd.cut(
    data["credit_score"],
    bins=[0, 600, 700, 750, 1000],
    labels=["Poor", "Average", "Good", "Excellent"]
)

print(
    data.groupby("credit_category", observed=True)["default_flag"]
    .mean().mul(100).round(2)
)

# Which age group has the highest loan default rate?
data["age_group"] = pd.cut(
    data["age"],
    bins=[0, 25, 35, 45, 60, 100],
    labels=["Below 25", "25-35", "36-45", "46-60", "Above 60"]
)

print(
    data.groupby("age_group", observed=True)["default_flag"]
    .mean().mul(100).round(2)
)

# Which states have the highest loan default rates?
print(
    data.groupby("state")["default_flag"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False)
)

# How many EMI instalments are paid, late, partial or missed?
print(
    repayments.groupby("payment_status")["repayment_id"]
    .count()
    .sort_values(ascending=False)
)

# Which loan delinquency category has the highest overdue amount?
print(
    loan_status.groupby("dpd_bucket")["overdue_amount_inr"]
    .sum().sort_values(ascending=False)
)

# Are larger loans more likely to default?
data["loan_range"] = pd.cut(
    data["principal_amount_inr"],
    bins=[0, 100000, 500000, 1000000, float("inf")],
    labels=["Below 1 Lakh", "1-5 Lakhs", "5-10 Lakhs", "Above 10 Lakhs"]
)

print(
    data.groupby("loan_range", observed=True)["default_flag"]
    .mean().mul(100).round(2)
)

# Are loans with higher interest rates more likely to default?
data["interest_range"] = pd.cut(
    data["annual_interest_rate_pct"],
    bins=[0, 10, 15, 20, float("inf")],
    labels=["Below 10%", "10-15%", "15-20%", "Above 20%"]
)

print(
    data.groupby("interest_range", observed=True)["default_flag"]
    .mean().mul(100).round(2)
)

# Are longer-tenure loans more likely to default?
data["tenure_group"] = pd.cut(
    data["tenure_months"],
    bins=[0, 12, 36, 60, float("inf")],
    labels=["Up to 1 Year", "1-3 Years", "3-5 Years", "Above 5 Years"]
)

print(
    data.groupby("tenure_group", observed=True)["default_flag"]
    .mean().mul(100).round(2)
)

# Which loan types have the highest outstanding overdue amounts?
print(
    data.groupby("loan_type")["overdue_amount_inr"]
    .sum().sort_values(ascending=False)
)

# Which cities have the highest loan default rates?
print(
    data.groupby("city")["default_flag"]
    .mean().mul(100).round(2)
    .sort_values(ascending=False)
)

data.to_csv("loan_analysis_data.csv", index=False)

print("Analysis data exported successfully!")

import matplotlib.pyplot as plt

chart = data.groupby("loan_type")["default_flag"].mean() * 100

chart.plot(kind="bar", title="Default Rate by Loan Type")

plt.ylabel("Default Rate (%)")
plt.xlabel("Loan Type")
plt.tight_layout()
plt.savefig("default_rate_by_loan_type.png")
plt.show()

chart = data.groupby("employment_type")["default_flag"].mean() * 100

chart.plot(kind="bar", title="Default Rate by Employment Type")

plt.ylabel("Default Rate (%)")
plt.xlabel("Employment Type")
plt.tight_layout()
plt.savefig("default_rate_by_employment.png")
plt.show()

chart = data.groupby("credit_category", observed=True)["default_flag"].mean() * 100

chart.plot(kind="bar", title="Default Rate by Credit Score")

plt.ylabel("Default Rate (%)")
plt.xlabel("Credit Category")
plt.tight_layout()
plt.savefig("default_rate_by_credit_score.png")
plt.show()

chart = data.groupby("dpd_bucket")["overdue_amount_inr"].sum()

chart.plot(kind="bar", title="Overdue Amount by DPD Bucket")

plt.ylabel("Overdue Amount (₹)")
plt.xlabel("DPD Bucket")
plt.tight_layout()
plt.savefig("overdue_by_dpd_bucket.png")
plt.show()

chart = data.groupby("loan_range", observed=True)["default_flag"].mean() * 100

chart.plot(kind="bar", title="Default Rate by Loan Amount")

plt.ylabel("Default Rate (%)")
plt.xlabel("Loan Amount")
plt.tight_layout()
plt.savefig("default_rate_by_loan_amount.png")
plt.show()

chart = data.groupby("state")["default_flag"].mean() * 100

chart.sort_values().plot(
    kind="bar",
    title="Default Rate by State"
)

plt.ylabel("Default Rate (%)")
plt.xlabel("State")
plt.tight_layout()
plt.savefig("default_rate_by_state.png")
plt.show()

chart = repayments["payment_status"].value_counts()

chart.plot(
    kind="bar",
    title="Repayment Performance"
)

plt.ylabel("Number of Installments")
plt.xlabel("Payment Status")
plt.tight_layout()
plt.savefig("repayment_performance.png")
plt.show()

chart = data.groupby("age_group", observed=True)["default_flag"].mean() * 100

chart.plot(
    kind="bar",
    title="Default Rate by Age Group"
)

plt.ylabel("Default Rate (%)")
plt.xlabel("Age Group")
plt.tight_layout()
plt.savefig("default_rate_by_age.png")
plt.show()

chart = data.groupby("loan_type")["overdue_amount_inr"].sum()

chart.sort_values().plot(
    kind="bar",
    title="Overdue Amount by Loan Type"
)

plt.ylabel("Overdue Amount (₹)")
plt.xlabel("Loan Type")
plt.tight_layout()
plt.savefig("overdue_by_loan_type.png")
plt.show()

chart = data.groupby("city")["default_flag"].mean() * 100

chart.sort_values().plot(
    kind="bar",
    title="Default Rate by City"
)

plt.ylabel("Default Rate (%)")
plt.xlabel("City")
plt.tight_layout()
plt.savefig("default_rate_by_city.png")
plt.show()

print(
    "Python Default Rate:",
    round(loan_status["default_flag"].mean() * 100, 2), "%"
)