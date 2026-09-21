# import pandas as pd

# # Load expense data
# df = pd.read_csv("expenses.csv")

# # Convert date column
# df["Date"] = pd.to_datetime(df["Date"])

# # Clean description
# df["Description"] = df["Description"].str.strip().str.lower()

# # Display data
# print("\nEXPENSE DATA")
# print(df)

# # Basic calculations
# total_expense = df["Amount"].sum()
# average_expense = df["Amount"].mean()
# number_of_transactions = len(df)

# print("\n----- EXPENSE SUMMARY -----")
# print("Total Expense:", total_expense)
# print("Average Expense:", round(average_expense, 2))
# print("Number of Transactions:", number_of_transactions) 

import pandas as pd


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("expenses.csv")

df["Date"] = pd.to_datetime(df["Date"])

df["Description"] = (
    df["Description"]
    .str.strip()
    .str.lower()
)


# ==========================================
# 2. EXPENSE CATEGORIES
# ==========================================

categories = {

    "Food": [
        "swiggy",
        "zomato",
        "restaurant",
        "canteen",
        "food",
        "lunch",
        "dinner"
    ],

    "Transport": [
        "uber",
        "ola",
        "metro",
        "bus",
        "petrol",
        "train",
        "taxi"
    ],

    "Shopping": [
        "amazon",
        "flipkart",
        "myntra",
        "clothes",
        "shoes",
        "electronics"
    ],

    "Entertainment": [
        "netflix",
        "spotify",
        "movie",
        "cinema",
        "game"
    ],

    "Education": [
        "book",
        "college",
        "course",
        "education"
    ],

    "Health": [
        "gym",
        "medicine",
        "hospital",
        "doctor"
    ]
}


# ==========================================
# 3. AUTOMATIC CATEGORIZATION
# ==========================================

def categorize_expense(description):

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in description:
                return category

    return "Others"


df["Category"] = df["Description"].apply(
    categorize_expense
)


# ==========================================
# 4. ANALYSIS
# ==========================================

total_expense = df["Amount"].sum()

average_expense = df["Amount"].mean()

number_of_transactions = len(df)


category_spending = (
    df.groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)


highest_category = category_spending.idxmax()


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("\n========== EXPENSE ANALYZER ==========")

print("\nExpense Data:")
print(df)

print("\nTotal Expense:")
print("₹", total_expense)

print("\nAverage Expense:")
print("₹", round(average_expense, 2))

print("\nNumber of Transactions:")
print(number_of_transactions)

print("\nCategory-wise Spending:")

print(category_spending)

print("\nHighest Spending Category:")
print(highest_category)

# ==========================================
# 6. MONTHLY ANALYSIS
# ==========================================

df["Month"] = df["Date"].dt.strftime("%Y-%m")

monthly_spending = (
    df.groupby("Month")["Amount"]
    .sum()
)


print("\nMonthly Spending:")

print(monthly_spending)

# ==========================================
# 7. BUDGET ANALYSIS
# ==========================================

monthly_budget = 20000

remaining_budget = monthly_budget - total_expense

budget_used_percentage = (
    total_expense / monthly_budget
) * 100


print("\nBudget:")
print("Monthly Budget: ₹", monthly_budget)

print("Spent: ₹", total_expense)

print("Remaining: ₹", remaining_budget)

print(
    "Budget Used:",
    round(budget_used_percentage, 2),
    "%"
)
# ==========================================
# 8. AUTOMATED INSIGHTS
# ==========================================

print("\n========== SMART INSIGHTS ==========")


# Highest spending category

print(
    f"💡 Your highest spending category is "
    f"{highest_category}."
)


# Budget warning

if budget_used_percentage >= 100:

    print(
        "🚨 You have exceeded your monthly budget."
    )

elif budget_used_percentage >= 80:

    print(
        "⚠️ You have used more than 80% "
        "of your monthly budget."
    )

else:

    print(
        "✅ Your spending is currently "
        "within your budget."
    )


# Category percentage

highest_category_amount = category_spending.iloc[0]

highest_category_percentage = (
    highest_category_amount /
    total_expense
) * 100


print(
    f"📊 {highest_category} accounts for "
    f"{highest_category_percentage:.1f}% "
    f"of your total spending."
)