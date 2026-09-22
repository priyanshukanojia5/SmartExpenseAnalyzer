"use client";

import { useState } from "react";

type Category = "Food" | "Transport" | "Shopping" | "Bills" | "Entertainment";

type Transaction = {
  id: number;
  merchant: string;
  description: string;
  amount: number;
  category: Category;
};

const initialTransactions: Transaction[] = [
  {
    id: 1,
    merchant: "Amazon",
    description: "Running shoes",
    amount: 2499,
    category: "Shopping",
  },
  {
    id: 2,
    merchant: "Uber",
    description: "Ride to college",
    amount: 320,
    category: "Transport",
  },
  {
    id: 3,
    merchant: "McDonald's",
    description: "Lunch",
    amount: 450,
    category: "Food",
  },
  {
    id: 4,
    merchant: "Netflix",
    description: "Monthly subscription",
    amount: 649,
    category: "Entertainment",
  },
  {
    id: 5,
    merchant: "Electricity Board",
    description: "Electricity bill",
    amount: 1200,
    category: "Bills",
  },
];

const categoryColors: Record<Category, string> = {
  Food: "bg-orange-500/10 text-orange-400",
  Transport: "bg-blue-500/10 text-blue-400",
  Shopping: "bg-purple-500/10 text-purple-400",
  Bills: "bg-red-500/10 text-red-400",
  Entertainment: "bg-pink-500/10 text-pink-400",
};

export default function Home() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [transactions, setTransactions] =
    useState<Transaction[]>(initialTransactions);

  const [merchant, setMerchant] = useState("");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");

  const [prediction, setPrediction] = useState<{
    category: string;
    confidence: number;
  } | null>(null);

  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const budget = 10000;

  const totalSpent = transactions.reduce(
    (total, transaction) => total + transaction.amount,
    0
  );

  const remaining = budget - totalSpent;

  const categoryTotals = transactions.reduce(
    (result, transaction) => {
      result[transaction.category] =
        (result[transaction.category] || 0) + transaction.amount;
      return result;
    },
    {} as Record<string, number>
  );

  async function predictCategory() {
    if (!merchant || !description) {
      setApiError("Enter both merchant and description.");
      return;
    }

    setLoading(true);
    setApiError("");
    setPrediction(null);

    try {
      const response = await fetch("http://127.0.0.1:8001/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          merchant,
          description,
        }),
      });

      if (!response.ok) {
        throw new Error("Prediction request failed");
      }

      const data = await response.json();

      setPrediction({
        category:
          data.category.charAt(0).toUpperCase() + data.category.slice(1),
        confidence: data.confidence,
      });
    } catch {
      setApiError(
        "Could not connect to SmartSpend AI API. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  function addExpense() {
    if (!merchant || !description || !amount) {
      setApiError("Please fill all expense fields.");
      return;
    }

    const category =
      prediction?.category && prediction.category in categoryColors
        ? (prediction.category as Category)
        : "Shopping";

    const newTransaction: Transaction = {
      id: Date.now(),
      merchant,
      description,
      amount: Number(amount),
      category,
    };

    setTransactions((current) => [newTransaction, ...current]);

    setMerchant("");
    setDescription("");
    setAmount("");
    setPrediction(null);
    setApiError("");
    setActivePage("Transactions");
  }

  function formatCurrency(value: number) {
    return `₹${value.toLocaleString("en-IN")}`;
  }

  return (
    <main className="min-h-screen bg-[#08090c] text-white">
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden w-64 flex-col border-r border-white/10 bg-[#0d0f13] p-5 md:flex">
          <div className="mb-10">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-black font-bold">
                S
              </div>

              <div>
                <h1 className="text-lg font-semibold">SmartSpend</h1>
                <p className="text-xs text-gray-500">AI Expense Analyzer</p>
              </div>
            </div>
          </div>

          <nav className="space-y-2">
            {["Dashboard", "Add Expense", "AI Categorizer", "Transactions"].map(
              (item) => (
                <button
                  key={item}
                  onClick={() => setActivePage(item)}
                  className={`w-full rounded-xl px-4 py-3 text-left text-sm transition ${
                    activePage === item
                      ? "bg-white text-black font-medium"
                      : "text-gray-400 hover:bg-white/5 hover:text-white"
                  }`}
                >
                  {item}
                </button>
              )
            )}
          </nav>

          <div className="mt-auto rounded-2xl border border-white/10 bg-white/[0.03] p-4">
            <p className="text-xs text-gray-500">SmartSpend AI</p>
            <p className="mt-1 text-sm text-gray-300">
              Intelligent spending insights
            </p>
            <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-white/10">
              <div className="h-full w-3/4 rounded-full bg-white" />
            </div>
          </div>
        </aside>

        {/* Main */}
        <section className="flex-1">
          {/* Header */}
          <header className="flex items-center justify-between border-b border-white/10 px-6 py-5 md:px-10">
            <div>
              <p className="text-sm text-gray-500">SmartSpend AI</p>
              <h2 className="mt-1 text-xl font-semibold">{activePage}</h2>
            </div>

            <div className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-white/5 text-sm">
              PK
            </div>
          </header>

          {/* Mobile nav */}
          <div className="flex gap-2 overflow-x-auto border-b border-white/10 p-4 md:hidden">
            {["Dashboard", "Add Expense", "AI Categorizer", "Transactions"].map(
              (item) => (
                <button
                  key={item}
                  onClick={() => setActivePage(item)}
                  className={`whitespace-nowrap rounded-lg px-3 py-2 text-xs ${
                    activePage === item
                      ? "bg-white text-black"
                      : "bg-white/5 text-gray-400"
                  }`}
                >
                  {item}
                </button>
              )
            )}
          </div>

          <div className="mx-auto max-w-7xl p-6 md:p-10">
            {/* Dashboard */}
            {activePage === "Dashboard" && (
              <div className="space-y-8">
                <div>
                  <p className="text-sm text-gray-500">Overview</p>
                  <h3 className="mt-1 text-3xl font-semibold tracking-tight">
                    Your spending at a glance.
                  </h3>
                  <p className="mt-2 text-gray-500">
                    Understand where your money is going with AI-powered
                    insights.
                  </p>
                </div>

                {/* KPI Cards */}
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <StatCard
                    title="Total Spending"
                    value={formatCurrency(totalSpent)}
                    subtitle="This month"
                  />

                  <StatCard
                    title="Monthly Budget"
                    value={formatCurrency(budget)}
                    subtitle="Your target"
                  />

                  <StatCard
                    title="Remaining"
                    value={formatCurrency(Math.max(remaining, 0))}
                    subtitle={remaining >= 0 ? "Within budget" : "Over budget"}
                  />

                  <StatCard
                    title="Transactions"
                    value={transactions.length.toString()}
                    subtitle="Recorded expenses"
                  />
                </div>

                {/* Budget */}
                <div className="rounded-2xl border border-white/10 bg-[#0d0f13] p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500">Budget health</p>
                      <h4 className="mt-1 text-xl font-semibold">
                        {remaining >= 0
                          ? "You're within your budget"
                          : "Budget exceeded"}
                      </h4>
                    </div>

                    <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                      {Math.round((totalSpent / budget) * 100)}% used
                    </span>
                  </div>

                  <div className="mt-5 h-3 overflow-hidden rounded-full bg-white/10">
                    <div
                      className="h-full rounded-full bg-white transition-all"
                      style={{
                        width: `${Math.min(
                          (totalSpent / budget) * 100,
                          100
                        )}%`,
                      }}
                    />
                  </div>

                  <div className="mt-3 flex justify-between text-xs text-gray-500">
                    <span>{formatCurrency(totalSpent)} spent</span>
                    <span>{formatCurrency(budget)} budget</span>
                  </div>
                </div>

                {/* Category + Recent */}
                <div className="grid gap-6 lg:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-[#0d0f13] p-6">
                    <div className="mb-6">
                      <p className="text-sm text-gray-500">Analytics</p>
                      <h4 className="mt-1 text-xl font-semibold">
                        Spending by category
                      </h4>
                    </div>

                    <div className="space-y-5">
                      {Object.entries(categoryTotals).map(
                        ([category, value]) => {
                          const percentage = (value / totalSpent) * 100;

                          return (
                            <div key={category}>
                              <div className="mb-2 flex justify-between text-sm">
                                <span className="text-gray-300">
                                  {category}
                                </span>
                                <span className="text-gray-500">
                                  {formatCurrency(value)}
                                </span>
                              </div>

                              <div className="h-2 rounded-full bg-white/10">
                                <div
                                  className="h-full rounded-full bg-white"
                                  style={{ width: `${percentage}%` }}
                                />
                              </div>
                            </div>
                          );
                        }
                      )}
                    </div>
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-[#0d0f13] p-6">
                    <div className="mb-6 flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-500">Activity</p>
                        <h4 className="mt-1 text-xl font-semibold">
                          Recent transactions
                        </h4>
                      </div>

                      <button
                        onClick={() => setActivePage("Transactions")}
                        className="text-xs text-gray-400 hover:text-white"
                      >
                        View all
                      </button>
                    </div>

                    <div className="space-y-4">
                      {transactions.slice(0, 5).map((transaction) => (
                        <TransactionRow
                          key={transaction.id}
                          transaction={transaction}
                          formatCurrency={formatCurrency}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Add Expense */}
            {activePage === "Add Expense" && (
              <div className="mx-auto max-w-2xl">
                <PageIntro
                  eyebrow="New transaction"
                  title="Add an expense."
                  description="Record a transaction and let SmartSpend AI categorize it."
                />

                <div className="mt-8 rounded-2xl border border-white/10 bg-[#0d0f13] p-6 md:p-8">
                  <ExpenseInputs
                    merchant={merchant}
                    description={description}
                    amount={amount}
                    setMerchant={setMerchant}
                    setDescription={setDescription}
                    setAmount={setAmount}
                  />

                  <button
                    onClick={async () => {
                      await predictCategory();
                    }}
                    className="mt-6 w-full rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black transition hover:bg-gray-200"
                  >
                    {loading ? "Analyzing..." : "Analyze Expense"}
                  </button>

                  {prediction && (
                    <PredictionCard prediction={prediction} />
                  )}

                  {apiError && (
                    <p className="mt-4 rounded-xl bg-red-500/10 p-3 text-sm text-red-400">
                      {apiError}
                    </p>
                  )}

                  {prediction && (
                    <button
                      onClick={addExpense}
                      className="mt-4 w-full rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-medium hover:bg-white/10"
                    >
                      Save Expense
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* AI Categorizer */}
            {activePage === "AI Categorizer" && (
              <div className="mx-auto max-w-2xl">
                <PageIntro
                  eyebrow="Machine learning"
                  title="AI expense categorizer."
                  description="Use your trained SmartSpend model to automatically classify expenses."
                />

                <div className="mt-8 rounded-2xl border border-white/10 bg-[#0d0f13] p-6 md:p-8">
                  <ExpenseInputs
                    merchant={merchant}
                    description={description}
                    amount=""
                    setMerchant={setMerchant}
                    setDescription={setDescription}
                    setAmount={() => {}}
                    hideAmount
                  />

                  <button
                    onClick={predictCategory}
                    className="mt-6 w-full rounded-xl bg-white px-5 py-3 text-sm font-semibold text-black hover:bg-gray-200"
                  >
                    {loading ? "AI is analyzing..." : "Predict Category"}
                  </button>

                  {prediction && (
                    <PredictionCard prediction={prediction} />
                  )}

                  {apiError && (
                    <p className="mt-4 rounded-xl bg-red-500/10 p-3 text-sm text-red-400">
                      {apiError}
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Transactions */}
            {activePage === "Transactions" && (
              <div>
                <PageIntro
                  eyebrow="History"
                  title="Your transactions."
                  description="Review the expenses recorded in SmartSpend AI."
                />

                <div className="mt-8 overflow-hidden rounded-2xl border border-white/10 bg-[#0d0f13]">
                  <div className="hidden grid-cols-5 border-b border-white/10 px-6 py-4 text-xs uppercase tracking-wider text-gray-500 md:grid">
                    <span>Merchant</span>
                    <span>Description</span>
                    <span>Category</span>
                    <span>Amount</span>
                    <span className="text-right">Status</span>
                  </div>

                  {transactions.map((transaction) => (
                    <div
                      key={transaction.id}
                      className="grid gap-3 border-b border-white/10 px-6 py-5 last:border-0 md:grid-cols-5 md:items-center"
                    >
                      <div>
                        <p className="font-medium">{transaction.merchant}</p>
                      </div>

                      <p className="text-sm text-gray-500">
                        {transaction.description}
                      </p>

                      <div>
                        <span
                          className={`rounded-full px-3 py-1 text-xs ${
                            categoryColors[transaction.category]
                          }`}
                        >
                          {transaction.category}
                        </span>
                      </div>

                      <p className="font-medium">
                        {formatCurrency(transaction.amount)}
                      </p>

                      <p className="text-left text-xs text-emerald-400 md:text-right">
                        Processed
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}

function StatCard({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: string;
  subtitle: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#0d0f13] p-5">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="mt-3 text-2xl font-semibold tracking-tight">{value}</p>
      <p className="mt-1 text-xs text-gray-600">{subtitle}</p>
    </div>
  );
}

function PageIntro({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <div>
      <p className="text-sm text-gray-500">{eyebrow}</p>
      <h3 className="mt-1 text-3xl font-semibold tracking-tight">{title}</h3>
      <p className="mt-2 max-w-2xl text-gray-500">{description}</p>
    </div>
  );
}

function ExpenseInputs({
  merchant,
  description,
  amount,
  setMerchant,
  setDescription,
  setAmount,
  hideAmount = false,
}: {
  merchant: string;
  description: string;
  amount: string;
  setMerchant: (value: string) => void;
  setDescription: (value: string) => void;
  setAmount: (value: string) => void;
  hideAmount?: boolean;
}) {
  return (
    <div className="space-y-5">
      <Input
        label="Merchant"
        placeholder="e.g. Amazon"
        value={merchant}
        onChange={setMerchant}
      />

      <Input
        label="Description"
        placeholder="e.g. Bought running shoes"
        value={description}
        onChange={setDescription}
      />

      {!hideAmount && (
        <Input
          label="Amount"
          placeholder="e.g. 2499"
          type="number"
          value={amount}
          onChange={setAmount}
        />
      )}
    </div>
  );
}

function Input({
  label,
  placeholder,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
}) {
  return (
    <div>
      <label className="mb-2 block text-sm text-gray-400">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none placeholder:text-gray-600 focus:border-white/30"
      />
    </div>
  );
}

function PredictionCard({
  prediction,
}: {
  prediction: { category: string; confidence: number };
}) {
  return (
    <div className="mt-6 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">
      <p className="text-xs uppercase tracking-wider text-emerald-400">
        AI prediction
      </p>

      <div className="mt-3 flex items-end justify-between">
        <div>
          <p className="text-2xl font-semibold">{prediction.category}</p>
          <p className="mt-1 text-sm text-gray-500">
            Classified by SmartSpend AI
          </p>
        </div>

        <p className="text-lg font-semibold text-emerald-400">
          {prediction.confidence.toFixed(2)}%
        </p>
      </div>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/10">
        <div
          className="h-full rounded-full bg-emerald-400"
          style={{
            width: `${Math.min(prediction.confidence, 100)}%`,
          }}
        />
      </div>
    </div>
  );
}

function TransactionRow({
  transaction,
  formatCurrency,
}: {
  transaction: Transaction;
  formatCurrency: (value: number) => string;
}) {
  return (
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium">{transaction.merchant}</p>
        <p className="mt-1 text-xs text-gray-600">
          {transaction.description}
        </p>
      </div>

      <div className="text-right">
        <p className="text-sm font-medium">
          {formatCurrency(transaction.amount)}
        </p>

        <span
          className={`mt-1 inline-block rounded-full px-2 py-0.5 text-[10px] ${
            categoryColors[transaction.category]
          }`}
        >
          {transaction.category}
        </span>
      </div>
    </div>
  );
}