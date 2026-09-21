import os
from datetime import date

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from insights import generate_insights


MODEL_FILE = "expense_classifier.pkl"
TRANSACTION_FILE = "transactions.csv"
SOURCE_FILE = "personal_expense.csv"

st.set_page_config(page_title="SmartSpend AI", page_icon="💰", layout="wide")

# ---------- Theme ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "sound" not in st.session_state:
    st.session_state.sound = True

dark = st.session_state.dark_mode
bg = "#070b16" if dark else "#f5f7fb"
card = "#111a2b" if dark else "#ffffff"
card2 = "#0d1424" if dark else "#f8fafc"
text = "#f8fafc" if dark else "#111827"
muted = "#a8b2c5" if dark else "#667085"
border = "#2a3852" if dark else "#e5e7eb"

theme_css = """
<style>
:root {
    --bg:__BG__;
    --card:__CARD__;
    --card2:__CARD2__;
    --text:__TEXT__;
    --muted:__MUTED__;
    --border:__BORDER__;
    --accent:#8b7cff;
}

/* App */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background:var(--bg) !important;
    color:var(--text) !important;
}

[data-testid="stAppViewContainer"] > .main {
    background:transparent !important;
}

.block-container {
    max-width:1400px;
    padding-top:1.5rem;
    padding-bottom:3rem;
}

/* Streamlit top bar */
header[data-testid="stHeader"] {
    background:var(--bg) !important;
    border-bottom:1px solid var(--border) !important;
    min-height:56px;
}

header[data-testid="stHeader"] button {
    color:var(--text) !important;
    opacity:1 !important;
}

header[data-testid="stHeader"]::after {
    content:"SMARTSPEND AI";
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    color:var(--text);
    font-size:.9rem;
    font-weight:850;
    letter-spacing:.18em;
    pointer-events:none;
}



/* Text */
h1,h2,h3,h4,h5,h6,p,span,label {
    color:var(--text) !important;
}

[data-testid="stCaptionContainer"] p,
small {
    color:var(--muted) !important;
}

/* Hero */
.smart-header {
    position:relative;
    overflow:hidden;
    padding:30px 32px;
    border:1px solid var(--border);
    border-radius:24px;
    margin:8px 0 24px;
    background:linear-gradient(135deg,rgba(139,124,255,.20),rgba(59,130,246,.08)),var(--card);
    box-shadow:0 18px 45px rgba(0,0,0,.16);
}

.smart-header::after {
    content:"";
    position:absolute;
    width:240px;
    height:240px;
    right:-80px;
    top:-110px;
    border-radius:50%;
    background:rgba(139,124,255,.16);
    filter:blur(12px);
}

.smart-header h1 {
    position:relative;
    z-index:1;
    margin:8px 0 4px;
    font-size:2.45rem !important;
    font-weight:850 !important;
    letter-spacing:-.03em;
}

.smart-header p {
    position:relative;
    z-index:1;
    margin:6px 0 0;
    color:var(--muted) !important;
}

.badge {
    display:inline-block;
    position:relative;
    z-index:1;
    padding:6px 11px;
    border-radius:999px;
    background:rgba(139,124,255,.15);
    color:#b6adff !important;
    font-size:.72rem;
    font-weight:850;
    letter-spacing:.07em;
}

/* Cards */
div[data-testid="stMetric"] {
    background:linear-gradient(145deg,var(--card),var(--card2)) !important;
    border:1px solid var(--border) !important;
    border-radius:18px !important;
    padding:18px !important;
    box-shadow:0 8px 26px rgba(0,0,0,.08);
    transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}

div[data-testid="stMetric"]:hover {
    transform:translateY(-5px);
    border-color:#6659c9 !important;
    box-shadow:0 18px 38px rgba(139,124,255,.16);
}

div[data-testid="stMetricLabel"] * {
    color:var(--muted) !important;
}

div[data-testid="stMetricValue"] {
    color:var(--text) !important;
    font-weight:850 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:var(--card) !important;
    border-right:1px solid var(--border) !important;
}

section[data-testid="stSidebar"] * {
    color:var(--text);
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color:var(--muted) !important;
}

/* Sidebar collapse/reopen control: large, visible, high contrast */
button[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button,
section[data-testid="stSidebar"] button[aria-label*="sidebar"],
header button[aria-label*="sidebar"] {
    color:var(--text) !important;
    background:var(--card) !important;
    border:1px solid var(--border) !important;
    opacity:1 !important;
    visibility:visible !important;
    z-index:999999 !important;
    border-radius:10px !important;
    box-shadow:0 4px 16px rgba(0,0,0,.18);
}

button[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
    color:#b6adff !important;
    border-color:#6659c9 !important;
}

/* Streamlit popovers and menus */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[role="menu"],
div[role="listbox"] {
    background:var(--card) !important;
    border:1px solid var(--border) !important;
    color:var(--text) !important;
}

div[data-baseweb="popover"] *,
div[data-baseweb="menu"] *,
div[role="menu"] *,
div[role="listbox"] * {
    color:var(--text) !important;
}

div[data-baseweb="popover"] [role="menuitem"]:hover,
div[data-baseweb="menu"] [role="option"]:hover,
div[role="menuitem"]:hover,
div[role="option"]:hover {
    background:rgba(139,124,255,.14) !important;
}

/* Native Streamlit tooltip/popover text */
div[data-testid="stTooltipContent"] {
    background:var(--card) !important;
    color:var(--text) !important;
}

/* Inputs - explicitly dark, fixing the white controls in dark mode */
div[data-baseweb="input"],
div[data-baseweb="input"] > div,
div[data-testid="stNumberInput"] > div,
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-testid="stFileUploader"] section {
    background:var(--card2) !important;
    border-color:var(--border) !important;
}

input, textarea {
    background:transparent !important;
    color:var(--text) !important;
    -webkit-text-fill-color:var(--text) !important;
}

input::placeholder,
textarea::placeholder {
    color:#7f8aa0 !important;
    opacity:1 !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] input,
[data-baseweb="select"] div {
    color:var(--text) !important;
}

[data-testid="stFileUploader"] {
    color:var(--text) !important;
}

[data-testid="stFileUploader"] section {
    border:1px solid var(--border) !important;
    border-radius:12px !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color:var(--muted) !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background:var(--card) !important;
    color:var(--text) !important;
    border:1px solid var(--border) !important;
    border-radius:12px !important;
    min-height:44px;
    font-weight:750;
    transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform:translateY(-2px);
    border-color:#6659c9 !important;
    box-shadow:0 10px 24px rgba(139,124,255,.16);
}

.stButton > button:active,
.stDownloadButton > button:active {
    transform:scale(.96);
}

/* Navigation */
div[role="radiogroup"] {
    gap:8px;
}

div[role="radiogroup"] label {
    color:var(--text) !important;
    font-weight:750;
    border-radius:12px;
}

/* Table */
div[data-testid="stDataFrame"] {
    border:1px solid var(--border);
    border-radius:14px;
    overflow:hidden;
}

/* Charts */
div[data-testid="stPlotlyChart"] {
    border:1px solid var(--border);
    border-radius:16px;
    overflow:hidden;
    background:var(--card);
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius:14px;
}

/* Divider */
hr {
    border-color:var(--border) !important;
    opacity:.75;
}

/* Workspace navigation */
.app-nav-title {
    color:var(--muted);
    font-size:.70rem;
    font-weight:850;
    letter-spacing:.14em;
    margin:8px 0 8px;
}
button[data-baseweb="tab"] {
    color:var(--muted) !important;
    background:transparent !important;
    border-radius:10px 10px 0 0 !important;
    font-weight:750 !important;
    padding:12px 18px !important;
}
button[data-baseweb="tab"]:hover {
    color:var(--text) !important;
    background:rgba(139,124,255,.08) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color:var(--text) !important;
    background:rgba(139,124,255,.12) !important;
}
div[data-baseweb="tab-highlight"] {
    background:#8b7cff !important;
    height:3px !important;
}

/* Number input: prevent white +/- controls in dark mode */
div[data-testid="stNumberInput"] button {
    background:var(--card2) !important;
    color:var(--text) !important;
    border-color:var(--border) !important;
}
div[data-testid="stNumberInput"] button:hover {
    background:rgba(139,124,255,.14) !important;
    color:var(--text) !important;
}
div[data-testid="stNumberInput"] [data-baseweb="input"] {
    background:var(--card2) !important;
}

/* File uploader */
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] section > div {
    background:var(--card2) !important;
    color:var(--text) !important;
}
div[data-testid="stFileUploader"] button {
    background:var(--card) !important;
    color:var(--text) !important;
    border:1px solid var(--border) !important;
}

/* Sidebar controls */
section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="input"] > div,
section[data-testid="stSidebar"] div[data-testid="stNumberInput"] button {
    background:var(--card2) !important;
    color:var(--text) !important;
    border-color:var(--border) !important;
}
section[data-testid="stSidebar"] input {
    color:var(--text) !important;
    -webkit-text-fill-color:var(--text) !important;
}

/* Toggle labels and controls */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] label {
    color:var(--text) !important;
}

/* Keep normal OS cursor; the animated ring is an overlay */
html, body, .stApp, .stApp * {
    cursor:auto !important;
}
button, a, [role="button"], input, textarea, select {
    cursor:pointer !important;
}
</style>
"""
theme_css = (theme_css
    .replace("__BG__", bg)
    .replace("__CARD__", card)
    .replace("__CARD2__", card2)
    .replace("__TEXT__", text)
    .replace("__MUTED__", muted)
    .replace("__BORDER__", border))
st.markdown(theme_css, unsafe_allow_html=True)


# Lightweight browser effects. The app keeps the normal OS pointer and adds
# a trailing ring; audio is generated only after a user interaction.
components.html("""
<script>
(function () {
  try {
    const doc = window.parent.document;
    if (doc.getElementById("smartspend-cursor")) return;

    const style = doc.createElement("style");
    style.id = "smartspend-cursor-style";
    style.textContent = `
      #smartspend-cursor {
        position:fixed;
        width:26px;height:26px;
        border:2px solid #8b7cff;
        border-radius:50%;
        pointer-events:none;
        z-index:2147483647;
        transform:translate(-50%,-50%);
        box-shadow:0 0 0 5px rgba(139,124,255,.10), 0 0 20px rgba(139,124,255,.30);
        transition:width .16s ease,height .16s ease,border-color .16s ease,box-shadow .16s ease;
      }
      #smartspend-cursor-dot {
        position:fixed;
        width:5px;height:5px;
        background:#8b7cff;
        border-radius:50%;
        pointer-events:none;
        z-index:2147483647;
        transform:translate(-50%,-50%);
        box-shadow:0 0 12px rgba(139,124,255,.75);
      }
      #smartspend-cursor.is-hover {
        width:36px;height:36px;
        border-color:#a99cff;
        box-shadow:0 0 0 7px rgba(139,124,255,.10), 0 0 28px rgba(139,124,255,.42);
      }
    `;
    doc.head.appendChild(style);

    const ring = doc.createElement("div");
    ring.id = "smartspend-cursor";
    const dot = doc.createElement("div");
    dot.id = "smartspend-cursor-dot";
    doc.body.appendChild(ring);
    doc.body.appendChild(dot);

    let x = innerWidth/2, y = innerHeight/2;
    let rx=x, ry=y;
    doc.addEventListener("mousemove", e => { x=e.clientX; y=e.clientY; }, {passive:true});
    function animate() {
      rx += (x-rx)*0.18;
      ry += (y-ry)*0.18;
      ring.style.left=rx+"px"; ring.style.top=ry+"px";
      dot.style.left=x+"px"; dot.style.top=y+"px";
      requestAnimationFrame(animate);
    }
    animate();

    doc.addEventListener("mouseover", e => {
      if (e.target.closest("button,a,[role='button'],input,select,textarea")) {
        ring.classList.add("is-hover");
      }
    });
    doc.addEventListener("mouseout", e => {
      if (e.target.closest("button,a,[role='button'],input,select,textarea")) {
        ring.classList.remove("is-hover");
      }
    });

    doc.addEventListener("pointerdown", e => {
      if (!e.target.closest("button,a,[role='button'],input,select,textarea")) return;
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!window.__smartspend_audio) window.__smartspend_audio = new AudioCtx();
        const ctx = window.__smartspend_audio;
        if (ctx.state === "suspended") ctx.resume();
        const o=ctx.createOscillator(), g=ctx.createGain();
        o.type="sine";
        o.frequency.setValueAtTime(560,ctx.currentTime);
        o.frequency.exponentialRampToValueAtTime(760,ctx.currentTime+.045);
        g.gain.setValueAtTime(.035,ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+.065);
        o.connect(g); g.connect(ctx.destination);
        o.start(); o.stop(ctx.currentTime+.065);
      } catch (_) {}
    }, true);
  } catch (_) {
    // Streamlit may sandbox component scripts; the app remains fully usable.
  }
})();
</script>
""", height=0)

# ---------- Data / ML helpers ----------
def load_model():
    return joblib.load(MODEL_FILE) if os.path.exists(MODEL_FILE) else None


def prepare_transaction_file():
    if os.path.exists(TRANSACTION_FILE):
        return

    if os.path.exists(SOURCE_FILE):
        df = pd.read_csv(SOURCE_FILE)
    else:
        df = pd.DataFrame(
            columns=["expense_id", "amount", "merchant",
                     "description", "category", "date"]
        )

    df.columns = df.columns.str.strip().str.lower()

    if "date" not in df.columns:
        df["date"] = pd.NaT

    df.to_csv(TRANSACTION_FILE, index=False)


KEYWORDS = {
    "Food": "swiggy zomato restaurant mcdonald starbucks canteen food lunch dinner breakfast coffee".split(),
    "Transport": "uber ola metro bus petrol shell train taxi fuel transport".split(),
    "Shopping": "amazon flipkart myntra clothes shoes shopping".split(),
    "Entertainment": "netflix spotify movie cinema game".split(),
    "Education": "book college course education study".split(),
    "Health": "gym medicine hospital doctor pharmacy".split(),
    "Technology": "apple electronics laptop phone technology".split(),
}


def keyword_category(merchant, description):
    text = f"{merchant} {description}".lower()
    for category, words in KEYWORDS.items():
        if any(word in text for word in words):
            return category
    return "Others"


def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file) if uploaded_file else pd.read_csv(TRANSACTION_FILE)
    df.columns = df.columns.str.strip().str.lower()

    aliases = {
        "expense": "amount", "value": "amount",
        "transaction_amount": "amount", "debit": "amount",
        "withdrawal": "amount", "details": "description",
        "transaction_details": "description", "narration": "description",
        "remarks": "description", "transaction_date": "date",
        "date_of_transaction": "date",
    }

    for old, new in aliases.items():
        if new not in df.columns and old in df.columns:
            df.rename(columns={old: new}, inplace=True)

    if "amount" not in df.columns:
        st.error(f"Amount column not found. Available columns: {list(df.columns)}")
        st.stop()

    if "description" not in df.columns:
        df["description"] = ""
    if "merchant" not in df.columns:
        df["merchant"] = "Unknown"

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    df = df[df["amount"] >= 0].copy()
    df["description"] = df["description"].fillna("").astype(str).str.strip()
    df["merchant"] = df["merchant"].fillna("Unknown").astype(str).str.strip()

    if "category" in df.columns:
        df["Category"] = df["category"].fillna("Others").astype(str).str.strip().str.title()
    else:
        df["Category"] = df.apply(
            lambda r: keyword_category(r["merchant"], r["description"]), axis=1
        )

    if "date" not in df.columns:
        df["date"] = pd.NaT
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


def predict_category(model, merchant, description):
    if model is None:
        return keyword_category(merchant, description), 0

    text = f"{merchant} {description}".strip()
    prediction = model.predict([text])[0].title()
    confidence = model.predict_proba([text])[0].max() * 100
    return prediction, confidence


def next_expense_id(df):
    if "expense_id" not in df.columns or df.empty:
        return "EXP1"

    numbers = pd.to_numeric(
        df["expense_id"].astype(str).str.extract(r"(\d+)")[0],
        errors="coerce",
    ).dropna()

    return f"EXP{int(numbers.max()) + 1}" if not numbers.empty else "EXP1"


def confidence_label(confidence):
    if confidence >= 80:
        return "🟢 High confidence"
    if confidence >= 50:
        return "🟡 Moderate confidence"
    return "🔴 Low confidence — verify the category"


# ---------- Dashboard sections ----------
def show_forecast(df, budget):
    if budget <= 0:
        st.info("Set a monthly budget greater than ₹0 to enable budget analysis.")
        return

    dated = df.dropna(subset=["date"])
    if dated.empty:
        st.info("📅 Add valid transaction dates to generate a spending forecast.")
        return

    days = max((dated["date"].max() - dated["date"].min()).days + 1, 1)
    daily = dated["amount"].sum() / days
    projected = daily * dated["date"].max().days_in_month

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Daily Spending", f"₹{daily:,.2f}")
    c2.metric("Projected Monthly Spending", f"₹{projected:,.2f}")
    c3.metric("Monthly Budget", f"₹{budget:,.2f}")

    if projected > budget:
        st.error(f"🚨 Projected spending is ₹{projected - budget:,.2f} above your budget.")
    elif projected >= budget * .8:
        st.warning("⚠️ You are approaching your monthly budget.")
    else:
        st.success("✅ Projected spending is currently within your budget.")


def show_trends(df):
    dated = df.dropna(subset=["date"])
    if dated.empty:
        st.info("📅 Add transaction dates to enable weekly and monthly analysis.")
        return

    monthly = (
        dated.assign(Month=dated["date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)["amount"].sum()
    )
    weekly = (
        dated.assign(Week=dated["date"].dt.to_period("W").astype(str))
        .groupby("Week", as_index=False)["amount"].sum()
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 📅 Monthly Spending")
        fig = px.bar(monthly, x="Month", y="amount", text_auto=".0f",
                     labels={"amount": "Spending (₹)"})
        fig.update_layout(template="plotly_dark" if dark else "plotly_white",
                          margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### 📆 Weekly Spending")
        fig = px.line(weekly, x="Week", y="amount", markers=True,
                      labels={"amount": "Spending (₹)"})
        fig.update_layout(template="plotly_dark" if dark else "plotly_white",
                          margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    if len(monthly) >= 2 and monthly.iloc[-2]["amount"] > 0:
        previous, current = monthly.iloc[-2]["amount"], monthly.iloc[-1]["amount"]
        change = (current - previous) / previous * 100
        c1, c2, c3 = st.columns(3)
        c1.metric("Previous Month", f"₹{previous:,.2f}")
        c2.metric("Current Month", f"₹{current:,.2f}")
        c3.metric("Change", f"{change:+.1f}%")


def show_anomalies(df):
    if len(df) < 3:
        st.info("Add at least 3 transactions to enable unusual spending detection.")
        return

    mean = df["amount"].mean()
    std = df["amount"].std()
    threshold = mean + 2 * (0 if pd.isna(std) else std)
    unusual = df[df["amount"] > threshold]

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Transaction", f"₹{mean:,.2f}")
    c2.metric("Unusual Threshold", f"₹{threshold:,.2f}")
    c3.metric("Unusual Transactions", len(unusual))

    if unusual.empty:
        st.success("✅ No unusually large transactions were detected.")
        return

    st.warning(f"⚠️ {len(unusual)} unusually large transaction(s) detected.")

    cols = [c for c in [
        "expense_id", "date", "merchant", "description", "amount", "Category"
    ] if c in unusual.columns]
    st.dataframe(unusual[cols], use_container_width=True, hide_index=True)


def dashboard_page(df, budget):
    total = df["amount"].sum()
    average = df["amount"].mean()
    count = len(df)
    remaining = budget - total
    used = total / budget * 100 if budget else 0

    st.markdown("""
    <div class="smart-header">
        <span class="badge">AI-POWERED PERSONAL FINANCE</span>
        <h1>💰 SmartSpend AI</h1>
        <p>Understand your spending. Discover patterns. Make smarter decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Spending", f"₹{total:,.2f}")
    c2.metric("📈 Average Expense", f"₹{average:,.2f}")
    c3.metric("🧾 Transactions", count)
    c4.metric("💵 Remaining Budget", f"₹{remaining:,.2f}")

    st.divider()
    st.subheader("🎯 Smart Budget Health")

    if budget > 0:
        st.progress(min(used / 100, 1))
        c1, c2, c3 = st.columns(3)
        c1.metric("Budget Used", f"{used:.1f}%")
        c2.metric("Amount Spent", f"₹{total:,.2f}")
        c3.metric("Remaining", f"₹{max(remaining, 0):,.2f}")
        show_forecast(df, budget)

    st.divider()
    st.subheader("📊 Spending Analysis")

    category = df.groupby("Category")["amount"].sum().sort_values(ascending=False)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🍩 Spending by Category")
        fig = px.pie(values=category.values, names=category.index, hole=.5)
        fig.update_layout(template="plotly_dark" if dark else "plotly_white",
                          margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### 💸 Category Comparison")
        fig = px.bar(x=category.index, y=category.values,
                     labels={"x": "Category", "y": "Amount (₹)"})
        fig.update_layout(template="plotly_dark" if dark else "plotly_white",
                          margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("📈 Spending Trends")
    show_trends(df)

    st.divider()
    st.subheader("🚨 Unusual Spending Detection")
    st.caption("Flags transactions above mean + 2 standard deviations.")
    show_anomalies(df)

    st.divider()
    st.subheader("🧠 Smart Spending Insights")
    for insight in generate_insights(df, budget):
        fn = {
            "danger": st.error,
            "warning": st.warning,
            "success": st.success,
            "info": st.info,
        }.get(insight["type"], st.info)
        fn(insight["message"])

    if not category.empty and total:
        top = category.index[0]
        pct = category.iloc[0] / total * 100
        st.divider()
        st.subheader("💡 Personalized Recommendation")
        if pct >= 40:
            st.warning(f"{top} accounts for {pct:.1f}% of spending. Consider reviewing this category.")
        elif pct >= 30:
            st.info(f"{top} is your largest category at {pct:.1f}%. Keep monitoring it.")
        else:
            st.success(f"Your spending is relatively distributed; {top} is largest at {pct:.1f}%.")


def add_expense_page(model):
    st.markdown("""
    <div class="smart-header">
        <span class="badge">AUTOMATED CATEGORIZATION</span>
        <h1>➕ Add New Expense</h1>
        <p>Enter a transaction and let the ML model classify it.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_expense"):
        c1, c2 = st.columns(2)
        merchant = c1.text_input("Merchant", placeholder="Amazon")
        description = c2.text_input("Description", placeholder="Bought headphones")
        c3, c4 = st.columns(2)
        amount = c3.number_input("Amount (₹)", min_value=0.0, step=10.0)
        transaction_date = c4.date_input("Transaction Date", value=date.today())
        submitted = st.form_submit_button("💾 Analyze & Save", type="primary")

    if not submitted:
        return

    if not merchant.strip() or not description.strip():
        st.warning("Please enter merchant and description.")
        return
    if amount <= 0:
        st.warning("Please enter an amount greater than ₹0.")
        return

    category, confidence = predict_category(model, merchant, description)
    saved = pd.read_csv(TRANSACTION_FILE)
    saved.columns = saved.columns.str.strip().str.lower()

    row = {
        "expense_id": next_expense_id(saved),
        "amount": amount,
        "merchant": merchant.strip(),
        "description": description.strip(),
        "category": category,
        "date": str(transaction_date),
    }

    saved = pd.concat([saved, pd.DataFrame([row])], ignore_index=True)
    saved.to_csv(TRANSACTION_FILE, index=False)

    st.success("✅ Expense saved successfully!")
    c1, c2 = st.columns(2)
    c1.metric("🤖 AI Category", category)
    c2.metric("AI Confidence", f"{confidence:.2f}%")
    st.caption(f"Transaction ID: {row['expense_id']} • {confidence_label(confidence)}")


def ai_categorizer_page(model):
    st.markdown("""
    <div class="smart-header">
        <span class="badge">MACHINE LEARNING</span>
        <h1>🤖 AI Expense Categorizer</h1>
        <p>TF-IDF + Logistic Regression predicts the expense category.</p>
    </div>
    """, unsafe_allow_html=True)

    if model is None:
        st.warning("ML model not found. Run train_model.py first.")
        return

    c1, c2 = st.columns(2)
    merchant = c1.text_input("Merchant", placeholder="Uber")
    description = c2.text_input("Description", placeholder="Ride to college")

    if st.button("🔮 Predict Category", type="primary"):
        if not merchant.strip() or not description.strip():
            st.warning("Please enter both fields.")
            return

        category, confidence = predict_category(model, merchant, description)
        c1, c2 = st.columns(2)
        c1.metric("Predicted Category", category)
        c2.metric("Confidence", f"{confidence:.2f}%")
        st.info(confidence_label(confidence))


def transactions_page(df):
    st.markdown("""
    <div class="smart-header">
        <span class="badge">DATA EXPLORER</span>
        <h1>📋 Transactions</h1>
        <p>Filter, inspect and export your expense history.</p>
    </div>
    """, unsafe_allow_html=True)

    selected = st.selectbox(
        "Filter by Category",
        ["All"] + sorted(df["Category"].unique()),
    )
    filtered = df if selected == "All" else df[df["Category"] == selected]

    cols = [c for c in [
        "expense_id", "date", "merchant", "description", "amount", "Category"
    ] if c in filtered.columns]

    st.dataframe(filtered[cols], use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "analyzed_expenses.csv",
        "text/csv",
    )


# ---------- App ----------
model = load_model()
prepare_transaction_file()

with st.sidebar:
    st.markdown("## 💠 SmartSpend AI")
    st.caption("Personal Finance Intelligence")
    st.divider()

    monthly_budget = st.number_input(
        "Monthly Budget (₹)",
        min_value=0,
        value=20000,
        step=1000,
    )

    uploaded_file = st.file_uploader("📂 Upload Expense CSV", type="csv")

    st.divider()
    st.markdown("### 🎨 Appearance")

    st.toggle(
        "🌙 Dark mode",
        key="dark_mode",
        help="Switch between light and dark themes.",
    )

    st.caption("Interactive cursor and click feedback are enabled in the browser.")

df = load_data(uploaded_file)

st.markdown('<div class="app-nav-title">WORKSPACE</div>', unsafe_allow_html=True)
tab_dashboard, tab_add, tab_ai, tab_transactions = st.tabs(
    ["📊 Dashboard", "➕ Add Expense", "🤖 AI Categorizer", "📋 Transactions"]
)

with tab_dashboard:
    dashboard_page(df, monthly_budget)

with tab_add:
    add_expense_page(model)

with tab_ai:
    ai_categorizer_page(model)

with tab_transactions:
    transactions_page(df)

st.divider()
st.markdown(
    '<div style="text-align:center;color:var(--muted);padding:12px 0 4px;">'
    '<b>SMARTSPEND AI</b> · Personal Finance Intelligence'
    '<br><small>Python · Pandas · Scikit-learn · Streamlit · Plotly</small>'
    '</div>',
    unsafe_allow_html=True,
)
