import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

import joblib


# =========================================================
# 1. LOAD DATASET
# =========================================================

DATA_FILE = "personal_expense.csv"

df = pd.read_csv(DATA_FILE)

print("\n========== DATASET LOADED ==========")

print("Rows:", len(df))
print("Columns:", list(df.columns))


# =========================================================
# 2. CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# =========================================================
# 3. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "merchant",
    "description",
    "category"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Missing required column: {column}"
        )


# =========================================================
# 4. CLEAN DATA
# =========================================================

df = df.dropna(
    subset=[
        "merchant",
        "description",
        "category"
    ]
)


df["merchant"] = (
    df["merchant"]
    .astype(str)
    .str.strip()
    .str.lower()
)


df["description"] = (
    df["description"]
    .astype(str)
    .str.strip()
    .str.lower()
)


df["category"] = (
    df["category"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# =========================================================
# 5. CREATE INPUT TEXT
# =========================================================

df["text"] = (
    df["merchant"] +
    " " +
    df["description"]
)


# =========================================================
# 6. DISPLAY CATEGORIES
# =========================================================

print("\n========== CATEGORIES ==========")

print(
    df["category"].value_counts()
)


# =========================================================
# 7. INPUT AND TARGET
# =========================================================

X = df["text"]

y = df["category"]


# =========================================================
# 8. TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\n========== DATA SPLIT ==========")

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================================================
# 9. MACHINE LEARNING PIPELINE
# =========================================================

model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )

])


# =========================================================
# 10. TRAIN MODEL
# =========================================================

print("\n========== TRAINING MODEL ==========")

model.fit(
    X_train,
    y_train
)

print("Model training completed!")


# =========================================================
# 11. TEST MODEL
# =========================================================

y_pred = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n========== MODEL PERFORMANCE ==========")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# =========================================================
# 12. SAVE MODEL
# =========================================================

MODEL_FILE = "expense_classifier.pkl"

joblib.dump(
    model,
    MODEL_FILE
)


print("\n========== MODEL SAVED ==========")

print(
    f"Saved as: {MODEL_FILE}"
)


# =========================================================
# 13. TEST WITH NEW EXPENSES
# =========================================================

test_expenses = [

    "amazon bought running shoes",

    "mcdonalds dinner",

    "uber ride to college",

    "netflix monthly subscription",

    "apple store headphones",

    "starbucks coffee"

]


print("\n========== SAMPLE PREDICTIONS ==========")


predictions = model.predict(
    test_expenses
)


probabilities = model.predict_proba(
    test_expenses
)


for expense, prediction, probability in zip(
    test_expenses,
    predictions,
    probabilities
):

    confidence = probability.max() * 100

    print(
        f"\nExpense: {expense}"
    )

    print(
        f"Predicted Category: {prediction}"
    )

    print(
        f"Confidence: {confidence:.2f}%"
    )