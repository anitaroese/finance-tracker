import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

def load_data(file_path):
    # Load JSON file into a DataFrame
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df

def calculate_summary(df):
    # Calculate total income, total expenses, and net balance
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expenses = df[df['type'] == 'expense']['amount'].sum()
    net_balance = total_income - total_expenses
    return total_income, total_expenses, net_balance

def plot_spending_by_category(df):

    expenses = df[df['type'] == 'expense']
    expenses_grouped = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(expenses_grouped.index, expenses_grouped.values)
    ax.set_xlabel('Category')
    ax.set_ylabel('Total Expenses ($)')
    ax.set_title('Total Expenses by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_monthly_trends(df):

    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month

    expenses_monthly = df[df['type'] == 'expense']
    income_monthly = df[df['type'] == 'income']

    total_expense_per_month = expenses_monthly.groupby('month')['amount'].sum()
    total_income_per_month = income_monthly.groupby('month')['amount'].sum()
    total_income_per_month = total_income_per_month.reindex(total_expense_per_month.index, fill_value=0)

    month_names = {3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August'}
    months = [month_names[m] for m in total_income_per_month.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(months))  # position for each month
    width = 0.35  # width of each bar

    ax.bar(x - width/2, total_income_per_month.values, width, label='Income')
    ax.bar(x + width/2, total_expense_per_month.values, width, label='Expenses')

    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.legend()
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')
    ax.set_title('Monthly Income vs Expenses')
    plt.tight_layout()
    return fig

def plot_savings_rate(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month  

    expenses_monthly = df[df['type'] == 'expense']
    income_monthly = df[df['type'] == 'income']
    
    total_expense_per_month = expenses_monthly.groupby('month')['amount'].sum()
    total_income_per_month = income_monthly.groupby('month')['amount'].sum()

    savings_rate = (total_income_per_month - total_expense_per_month) / total_income_per_month * 100
    savings_rate = savings_rate.replace([np.inf, -np.inf], np.nan).dropna()

    month_names = {3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August'}
    months = [month_names[m] for m in savings_rate.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(months, savings_rate.values)

    ax.set_xlabel('Month')
    ax.set_ylabel('Savings Rate (%)')
    ax.set_title('Monthly Savings Rate')
    ax.axhline(y=20, color='orange', linestyle='--', label='Target: 20%')
    ax.legend()
    plt.tight_layout()

    return fig



def main():

    st.title("Finance Tracker Dashboard")

    df = load_data("finance_data.json")

    total_income, total_expenses, net_balance = calculate_summary(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Net Balance", f"${net_balance:,.2f}")

    st.dataframe(df)

    st.header("Spending by Category")
    st.pyplot(plot_spending_by_category(df))

    st.header("Monthly Trends")
    st.pyplot(plot_monthly_trends(df))

    st.header("Monthly Savings Rate")
    st.pyplot(plot_savings_rate(df))

    

if __name__ == "__main__":
    main()
