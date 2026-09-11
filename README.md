# Finance Tracker

An end-to-end personal finance pipeline built in Python. Transactions from March–May were logged manually via a CLI tool to validate the data structure; July–August were imported automatically from Capital One CSV exports and categorized using the Groq API. A Streamlit dashboard provides personal financial analysis across all data.

## Features

- Add income and expense transactions with date and category
- Persistent storage using JSON
- Export transaction history to CSV
- Summary view with total income, total expenses, and balance
- 8 expense categories: groceries, dining out, subscriptions, 
  entertainment, clothing, gifts, services, and other
- AI-powered Capital One CSV import with automatic transaction categorization (Groq API)

## Technologies

- Python 3
- Libraries: `json`, `csv`, `datetime`, `pandas`, `matplotlib`, `streamlit`, `groq`

## How to Run

```bash
python finance_tracker.py
```
## Live Demo
[View Dashboard](https://anita-roese-finance-tracker.streamlit.app/)

## Roadmap

- [x] Analysis layer using pandas and matplotlib
- [x] Interactive dashboard with Streamlit
- [ ] Multi-currency support (USD/BRL)

## Purpose

Built as a portfolio project while learning Python, with a focus 
on financial data — an area I'm pursuing professionally.