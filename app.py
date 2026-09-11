import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

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

def main():

    st.title("Finance Tracker Dashboard")

    df = load_data("finance_data.json")

    total_income, total_expenses, net_balance = calculate_summary(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Net Balance", f"${net_balance:,.2f}")

    st.dataframe(df)

    



if __name__ == "__main__":
    main()
