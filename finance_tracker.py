import json
import csv
from datetime import datetime

def load_data():
    """Return the data that already existed inside the finance_data.json file"""
    try:
        with open("finance_data.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
    
def save_data(transactions):
    """Save data into the finance_data.json file"""
    with open("finance_data.json", "w") as file:
        json.dump(transactions, file, indent=4)

def export_to_csv(transactions):
    """Export existed data into finance_data.csv file"""
    with open("finance_data.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["type", "name", "amount", "date", "category"])
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)

def get_number(prompt):
    """Prompt the user for a number, looping until valif float is entered"""
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid amount.")

def get_transaction(transaction_type):
    """Prompt the user for a transaction, storing the name, amount, type and date"""
    if transaction_type == "expense":
        while True:
            category = input("\nCategories: \n1. Groceries \n2. Dining out \n3. Subscriptions \n4. Entertainment \n5. Clothing \n6. Gifts \n7. Services \n8. Other \nChoose an option: ")

            if category == "1":
                transaction_category = "groceries"
                break
            elif category == "2":
                transaction_category = "dining out"
                break
            elif category == "3":
                transaction_category = "subscriptions"
                break
            elif category == "4":
                transaction_category = "entertainment"
                break
            elif category == "5":
                transaction_category = "clothing"
                break
            elif category == "6":
                transaction_category = "gifts"
                break
            elif category == "7":
                transaction_category = "services"
                break
            elif category == "8":
                transaction_category = "other"
                break
            else:
                print("Invalid choice")
            
    
    while True: 
        name = input("Enter transaction name: ").strip().lower()
        
        if name == "":
            print("Transaction name cannot be empty.")
        else:
            break

    while True: 
        amount = get_number(f"Enter amount for {name}: $")

        if amount <= 0:
            print("Amount must be greater than 0.")
        else:
            break

    while True:
        choice = input("Date (press Enter for today, or type in YYYY-MM-DD format):")
        if choice == "":
            date = datetime.now().strftime("%Y-%m-%d")
            break
        else:
            try:
                datetime.strptime(choice.strip(), "%Y-%m-%d") # check if user's input is valid by trying to convert it to datetime format
                date = choice
                break
            except ValueError:
                print("Invalid format")

    
    if transaction_type == "expense":
        transaction = {"type":transaction_type, "category": transaction_category, "name":name, "amount":amount, "date":date}
    else:
        transaction = {"type":transaction_type, "category":"", "name":name, "amount":amount, "date":date}

    return transaction

def show_summary(transactions):
    """Show summary of transactions including total expenses, total incomes, and balance"""
    total_expenses = 0
    total_income = 0
    expenses = []
    incomes = []

    for transaction in transactions:
        if transaction["type"] == "expense":
            total_expenses += transaction["amount"]
            expenses.append(f"{transaction['name']}: ${transaction['amount']:.2f}")
        else:
            total_income += transaction["amount"]
            incomes.append(f"{transaction['name']}: ${transaction['amount']:.2f}")

    balance = total_income - total_expenses

    print("\nExpenses:")
    for expense in expenses:
        print(expense)


    print("\nIncomes:")
    for income in incomes:
        print(income)


    print("\n---Summary---")
    print(f"Total incomes: ${total_income:.2f}")
    print(f"Total expenses: ${total_expenses:.2f}")

    if balance > 0: 
        print(f"Surplus: ${balance:.2f} ✅")
    elif balance < 0:
        print(f"Deficit: ${balance:.2f} ❌")
    else:
        print("Break-even: $0.00")



def main():
    transactions = load_data()

    while True:
        print("\n=== Finance Tracker ===")
        print("1. View current data")
        print("2. Add income")
        print("3. Add expense")
        print("4. Save data")
        print("5. Export to csv")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_summary(transactions)

        # transaction_type is inferred from menu choice, no need to ask the user explicitly
        elif choice == "2":
            transactions.append(get_transaction("income"))

        elif choice == "3":
            transactions.append(get_transaction("expense"))

        elif choice == "4":
            save_data(transactions)
            print("Data saved to finance_data.json")
        
        elif choice == "5":
            save_data(transactions)
            export_to_csv(transactions)
            print("Data exported to finance_data.csv")
        
        elif choice == "6": 
            save_data(transactions)
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")
    print("=== Finance Tracker ===")

    
if __name__ == "__main__":
    main()