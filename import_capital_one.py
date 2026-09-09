import pandas as pd
import json
from datetime import datetime

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

def main():
    file_path = 'C:\\Users\\anita\\OneDrive\\Documentos\\Projects\\finance-tracker\\2026-09-03_360Checking...1852.csv'
    df_capital_one = load_capital_one_csv(file_path)
    filtered_df = filter_capital_one_transactions(df_capital_one)
    converted_dates = filtered_df['Transaction Date'].apply(convert_date_format)
    filtered_df['Transaction Date'] = converted_dates

    cleaned_descriptions = filtered_df['Transaction Description'].apply(clean_description)
    filtered_df['Transaction Description'] = cleaned_descriptions 

    print(filtered_df)  


if __name__ == "__main__":
    main()