import streamlit as st
import pandas as pd
import datetime
import calendar
import plotly.express as px
from Expenses import Expense

# File path
expense_file_path = "expenses.csv"

# Load expenses from file
def load_expenses(path):
    try:
        df = pd.read_csv(path)
        if df.empty or df.isnull().all().all():
            return None
        df.columns = ["Name", "Category", "Amount", "Date"]
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except Exception as e:
        print(f"Error loading expenses: {e}")
        return None

# Save new expense to file
def save_expense(expense, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount},{expense.date}\n")

# Delete expense by index
def delete_expense(index, df, path):
    df = df.drop(index)
    df.to_csv(path, index=False)

# Reset all data
def reset_expenses(path):
    open(path, 'w').close()

# Monthly summaries from Jan 2025
def calculate_monthly_summaries(df):
    if df.empty or "Date" not in df.columns or "Amount" not in df.columns:
        return pd.DataFrame()

    df = df[df["Date"] >= pd.to_datetime("2025-01-01")]
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    grouped = df.groupby(["Year", "Month"])["Amount"].sum().reset_index()
    grouped["Month"] = grouped["Month"].apply(lambda x: calendar.month_name[x])
    return grouped

# Streamlit UI
st.set_page_config(page_title="Daily Expense Tracker", layout="centered")
st.title("💰 Daily Expense Tracker")

# ➕ Add New Expense
st.header("➕ Add New Expense")
with st.form("expense_form"):
    name = st.text_input("Expense Name")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["🍕Food", "🏠Home", "💼Work", "🎉Fun", "✨Misc"])
    date = st.date_input("Date", datetime.date.today())
    submitted = st.form_submit_button("Add Expense")

    if submitted and name and amount:
        expense = Expense(name, category, amount, date)
        save_expense(expense, expense_file_path)
        st.success(f"✅ Added: {expense.name} (${expense.amount}) to {expense.category}")
        st.rerun()

# 📄 Expense Summary
st.header("📄 Expense Summary")
expenses_df = load_expenses(expense_file_path)

if expenses_df is not None and not expenses_df.empty:
    st.subheader("🧾 All Expenses")

    # Display each expense with delete button
    for i in range(len(expenses_df)):
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 3, 2])
        col1.markdown(f"**{expenses_df['Name'][i]}**")
        col2.markdown(expenses_df["Category"][i])
        col3.markdown(f"${expenses_df['Amount'][i]:.2f}")
        date_val = expenses_df["Date"][i]
        col4.markdown(date_val.strftime("%Y-%m-%d") if pd.notnull(date_val) else "N/A")
        if col5.button("🗑️ Delete", key=f"del_{i}"):
            delete_expense(i, expenses_df, expense_file_path)
            st.rerun()

    # Pie Chart
    st.subheader("📊 Expenses by Category (Pie Chart)")
    category_summary = expenses_df.groupby("Category")["Amount"].sum()
    fig = px.pie(values=category_summary.values, names=category_summary.index,
                 title="Spending by Category", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # Total
    st.subheader("💸 Total Spent")
    total_spent = expenses_df["Amount"].sum()
    st.markdown(f"### **${total_spent:.2f}**")

    # Monthly Summary
    st.subheader("📆 Monthly Summary (from 2025 onwards)")
    monthly_summaries = calculate_monthly_summaries(expenses_df)

    if not monthly_summaries.empty:
        for _, row in monthly_summaries.iterrows():
            st.markdown(f"**{row['Month']} {row['Year']}:** ${row['Amount']:.2f}")
    else:
        st.info("No expense data available for 2025 or later.")

    if st.button("♻️ Reset All Data"):
        reset_expenses(expense_file_path)
        st.success("All expenses have been reset.")
        st.rerun()
else:
    st.info("There are currently no expenses added.")
