import json
import os

def load_data():
    if os.path.exists("finance_data.json"):
        with open("finance_data.json", "r") as file:
            data = json.load(file)
            return data["income"], data["expenses"]
    else:
        return 0, {}
    
def save_data(income, expenses):
    data = {
        "income": income,
        "expenses": expenses
    }

    with open("finance_data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid amount.")

def get_expense():
    while True: 
        name = input("Enter expense name (or 'done' to finish): ").strip().lower()

        if name == "done":
            return None
        
        if name == "":
            print("Expense name cannot be empty.")
            continue

        while True: 
            amount = get_number(f"Enter amount for {name}: $")

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            break

        return name, amount


def main():
    print("=== Finance Tracker ===")

    # Ask for income 
    income = get_number("Enter your total income for the month: $")

    # Collect expenses
    saved_income, expenses = load_data()

    while True:
        expense = get_expense()

        if expense is None:
            break

        name, amount = expense

        if name in expenses:
            # Combine expenses with the same category
            expenses[name] += amount
        else:
            expenses[name] = amount
    
    # Calculate total
    total_expenses = sum(expenses.values())
    balance = income - total_expenses

    print("\nExpenses:")
    for name, amount in expenses.items():
        print(f"{name.title()}: ${amount:.2f}")

    # Print summary
    print("\n--- Summary ---")
    print(f"Income: ${income:.2f}")
    print(f"Total expenses: ${total_expenses:.2f}")

    if balance > 0:
        print(f"Surplus: ${balance:.2f} ✅")
    elif balance < 0:
        print(f"Deficit: ${abs(balance):.2f}  ❌")
    else:
        print("Break-even: $0.00")

    save_data(income, expenses)
    print("\nData saved to finance_data.json")
    
main()