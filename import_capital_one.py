import pandas as pd
import json
from datetime import datetime
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

CATEGORY_RULES = {
    'dining out': ['chipotle', 'starbucks', 'panera', 'shugs', 'chick fil', 'pizza', 'smoothie', 'rue de la course', 'cava', 'uber eats'],
    'groceries': ['wm supercenter', 'target', 'publix', 'fresh market'],
    'subscriptions': ['visible', 'apple com bill', 'chatgpt', 'openai', 'uber one', 'amazon prime'],
    'entertainment': ['airbnb', 'delta air', 'partners on booking'],
    'clothing': ['old navy', 'tj maxx', 'amazon', 'goodwill'],
    'gifts': [],
    'services': ['ussf', 'taxes'],
    'other': ['shell', 'pilot', 'venmo', 'zelle']
}

def load_capital_one_csv(file_path):
    df_capital_one = pd.read_csv(file_path)
    return df_capital_one

def filter_capital_one_transactions(df_capital_one):
    # Filter out rows where 'Transaction Description' contains '360 Performance Savings', '360 Checking', or 'Monthly Interest'
    filtered_df = df_capital_one[~df_capital_one['Transaction Description'].str.contains('360 Performance Savings|360 Checking|Monthly Interest', case=False, na=False)]
    return filtered_df

def convert_date_format(date_str):
    # Convert date from 'MM/DD/YYYY' to 'YYYY-MM-DD'
    try:
        date_obj = datetime.strptime(date_str, '%m/%d/%y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return date_str  # Return the original string if it doesn't match the expected format

def clean_description(description):
    # Remove text before '-' and numbers at the end
    cleaned_description = description.split('-')[-1].strip()  # Keep text after the last '-'
    cleaned_description = ''.join([i for i in cleaned_description if not i.isdigit()]).strip()  # Remove digits
    return cleaned_description

def categorize_transaction(description):
    description = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'other'

def categorize_with_ai(description):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Classify this bank transaction into exactly one of these categories:
groceries, dining out, subscriptions, entertainment, clothing, gifts, services, other.

Transaction: {description}

Return only the category name, nothing else."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip().lower()

def review_transactions(df):
    for index, row in df.iterrows():
        if row['Transaction Type'] != 'Credit':
            print(f"Transaction Description: {row['Transaction Description']}")
            print(f"Category: {row['Category']}")
            print(f"Transaction Date: {row['Transaction Date']}")
            print(f"Transaction Amount: {row['Transaction Amount']}")
            user_input = input("Is this categorization correct? (y/n): ")
            if user_input.lower() == 'n':
                new_category = input("Please choose the correct category: 1. groceries, 2. dining out, 3. subscriptions, 4. entertainment, 5. clothing, 6. gifts, 7. services, 8. other: ")
                category_mapping = {
                    '1': 'groceries',
                    '2': 'dining out',
                    '3': 'subscriptions',
                    '4': 'entertainment',
                    '5': 'clothing',
                    '6': 'gifts',
                    '7': 'services',
                    '8': 'other'
                }
                df.at[index, 'Category'] = category_mapping.get(new_category, 'other')

    return df

def convert_to_tracker_format(df):
    # Convert the DataFrame to the desired format for finance-tracker
    transactions = []
    for index, row in df.iterrows():
        transaction = {
            "type": "expense" if row['Transaction Type'] != 'Credit' else "income",
            "category": row['Category'],
            "name": row['Transaction Description'],
            "amount": row['Transaction Amount'],
            "date": row['Transaction Date']     
        }
        transactions.append(transaction)

    return transactions

def main():
    file_path = 'C:\\Users\\anita\\OneDrive\\Documentos\\Projects\\finance-tracker\\capital_one_script.csv'
    df_capital_one = load_capital_one_csv(file_path)
    filtered_df = filter_capital_one_transactions(df_capital_one)
    converted_dates = filtered_df['Transaction Date'].apply(convert_date_format)
    filtered_df['Transaction Date'] = converted_dates

    cleaned_descriptions = filtered_df['Transaction Description'].apply(clean_description)
    filtered_df['Transaction Description'] = cleaned_descriptions 

    categorized_transactions = filtered_df['Transaction Description'].apply(categorize_transaction)
    filtered_df['Category'] = categorized_transactions

    filtered_df['Category'] = filtered_df['Transaction Description'].apply(categorize_with_ai)

    print(filtered_df)

    review_transactions(filtered_df)


if __name__ == "__main__":
    main()