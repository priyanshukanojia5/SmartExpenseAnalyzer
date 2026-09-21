import pandas as pd


def generate_insights(
    df,
    monthly_budget
):

    insights = []


    # =====================================================
    # BASIC VALUES
    # =====================================================

    total_spending = df["amount"].sum()

    transaction_count = len(df)

    average_transaction = (
        df["amount"].mean()
        if transaction_count > 0
        else 0
    )


    # =====================================================
    # 1. HIGHEST SPENDING CATEGORY
    # =====================================================

    category_totals = (
        df.groupby("Category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    if len(category_totals) > 0:

        highest_category = (
            category_totals.index[0]
        )

        highest_category_amount = (
            category_totals.iloc[0]
        )

        category_percentage = (
            highest_category_amount /
            total_spending
        ) * 100


        insights.append({

            "type": "category",

            "message":
            f"🏆 {highest_category} is your "
            f"highest spending category, "
            f"accounting for "
            f"{category_percentage:.1f}% "
            f"of your total spending."

        })


    # =====================================================
    # 2. BUDGET ANALYSIS
    # =====================================================

    if monthly_budget > 0:

        budget_percentage = (
            total_spending /
            monthly_budget
        ) * 100


        if budget_percentage >= 100:

            insights.append({

                "type": "danger",

                "message":
                f"🚨 You have exceeded your "
                f"monthly budget by "
                f"₹{total_spending - monthly_budget:,.2f}."

            })


        elif budget_percentage >= 80:

            insights.append({

                "type": "warning",

                "message":
                f"⚠️ You have used "
                f"{budget_percentage:.1f}% "
                f"of your monthly budget. "
                f"Only ₹"
                f"{monthly_budget - total_spending:,.2f} "
                f"remains."

            })


        else:

            insights.append({

                "type": "success",

                "message":
                f"✅ You have used "
                f"{budget_percentage:.1f}% "
                f"of your monthly budget."

            })


    # =====================================================
    # 3. LARGE TRANSACTION DETECTION
    # =====================================================

    large_transaction_limit = (
        average_transaction * 2
    )


    large_transactions = df[
        df["amount"] >
        large_transaction_limit
    ]


    if len(large_transactions) > 0:

        insights.append({

            "type": "warning",

            "message":
            f"⚠️ You have "
            f"{len(large_transactions)} "
            f"transaction(s) that are more than "
            f"twice your average transaction."

        })


    # =====================================================
    # 4. TRANSACTION COUNT
    # =====================================================

    if transaction_count > 0:

        insights.append({

            "type": "info",

            "message":
            f"🧾 You made "
            f"{transaction_count} transactions "
            f"with an average value of "
            f"₹{average_transaction:,.2f}."

        })


    # =====================================================
    # 5. CATEGORY DIVERSITY
    # =====================================================

    number_of_categories = (
        df["Category"].nunique()
    )


    insights.append({

        "type": "info",

        "message":
        f"📊 Your expenses are distributed "
        f"across "
        f"{number_of_categories} "
        f"categories."

    })
    # =====================================================
    # 6. SPENDING TREND
    # =====================================================

    if "date" in df.columns:

        temp_df = df.copy()

        temp_df["date"] = pd.to_datetime(
            temp_df["date"],
            errors="coerce"
        )

        temp_df = temp_df.dropna(
            subset=["date"]
        )


        if len(temp_df) > 0:

            temp_df["month"] = (
                temp_df["date"]
                .dt.to_period("M")
            )


            monthly_spending = (
                temp_df
                .groupby("month")["amount"]
                .sum()
                .sort_index()
            )


            if len(monthly_spending) >= 2:

                current_month = (
                    monthly_spending.iloc[-1]
                )

                previous_month = (
                    monthly_spending.iloc[-2]
                )


                if previous_month > 0:

                    change = (
                        (
                            current_month -
                            previous_month
                        )
                        /
                        previous_month
                    ) * 100


                    if change > 0:

                        insights.append({

                            "type": "warning",

                            "message":
                            f"📈 Spending increased by "
                            f"{change:.1f}% compared "
                            f"with the previous month."

                        })


                    elif change < 0:

                        insights.append({

                            "type": "success",

                            "message":
                            f"📉 Spending decreased by "
                            f"{abs(change):.1f}% compared "
                            f"with the previous month."

                        })


                    else:

                        insights.append({

                            "type": "info",

                            "message":
                            "➡️ Spending remained "
                            "almost unchanged compared "
                            "with the previous month."

                        })

    return insights