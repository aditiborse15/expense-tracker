import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tracker import ExpenseTracker, initialize_file

# ── Setup ──
initialize_file()
tracker = ExpenseTracker()

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Expense Tracker")

# ── Sidebar: Add Expense ──
st.sidebar.header("➕ Add New Expense")
category = st.sidebar.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"])
amount = st.sidebar.number_input("Amount (₹)", min_value=1, step=1)
description = st.sidebar.text_input("Description")
budget = st.sidebar.number_input("Monthly Budget (₹)", min_value=0, step=100, value=5000)

if st.sidebar.button("Add Expense"):
    if description.strip() == "":
        st.sidebar.error("Please enter a description.")
    else:
        tracker.add_expense(category, amount, description)
        st.sidebar.success("✅ Expense added!")
        st.rerun()

# ── Load Data ──
expenses = tracker.get_all_expenses()

if not expenses:
    st.info("No expenses yet. Add one from the sidebar!")
else:
    df = pd.DataFrame(expenses)
    df["Amount"] = pd.to_numeric(df["Amount"])
    df["Date"] = pd.to_datetime(df["Date"])

    # ── Filters ──
    st.subheader("🔍 Filters")
    col1, col2 = st.columns(2)

    with col1:
        months = ["All"] + sorted(df["Date"].dt.strftime("%B %Y").unique().tolist())
        selected_month = st.selectbox("Filter by Month", months)

    with col2:
        categories = ["All"] + sorted(df["Category"].unique().tolist())
        selected_cat = st.selectbox("Filter by Category", categories)

    # Apply filters
    filtered = df.copy()
    if selected_month != "All":
        filtered = filtered[filtered["Date"].dt.strftime("%B %Y") == selected_month]
    if selected_cat != "All":
        filtered = filtered[filtered["Category"] == selected_cat]

    # ── Summary Cards ──
    st.subheader("📊 Summary")
    total = filtered["Amount"].sum()
    highest = filtered["Amount"].max()
    count = len(filtered)
    remaining = budget - total

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Spent", f"₹{total:,.0f}")
    c2.metric("Transactions", count)
    c3.metric("Highest Expense", f"₹{highest:,.0f}")
    c4.metric("Budget Remaining", f"₹{remaining:,.0f}",
              delta=f"₹{remaining:,.0f}",
              delta_color="normal" if remaining >= 0 else "inverse")

    # Budget Alert
    if budget > 0 and total >= budget:
        st.error(f"⚠️ Budget exceeded! You spent ₹{total:,.0f} out of ₹{budget:,.0f}")
    elif budget > 0 and total >= budget * 0.8:
        st.warning(f"⚠️ 80% of budget used! ₹{remaining:,.0f} remaining.")

    # ── Pie Chart ──
    st.subheader("🥧 Spending by Category")
    cat_totals = filtered.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(cat_totals, labels=cat_totals.index, autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

    # ── Expense Table ──
    st.subheader("📋 Expense List")
    display_df = filtered[["No", "Date", "Category", "Amount", "Description"]].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # ── Delete Expense ──
    st.subheader("🗑️ Delete Expense")
    expense_no = st.number_input("Enter Expense No. to delete", min_value=1, step=1)
    if st.button("Delete"):
        tracker.delete_expense(expense_no)
        st.success("✅ Expense deleted!")
        st.rerun()