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

def show_summary(income, expenses):
    total_expenses = sum(expenses.values())
    balance = income - total_expenses

    print("\nExpenses:")
    if expenses:
        for name, amount in expenses.items():
            print(f"{name.title()}: ${amount:.2f}")
    else:
        print("No expenses recorded.")

    print("\n---Summary---")
    print(f"Income: ${income:.2f}")
    print(f"Total expenses: ${total_expenses:.2f}")

    if balance > 0: 
        print(f"Surplus: ${balance:.2f} ✅")
    elif balance < 0:
        print(f"Deficit: ${balance:.2f} ❌")
    else:
        print("Break-even: $0.00")



def main():
    income, expenses = load_data()

    while True:
        print("\n=== Finance Tracker ===")
        print("1. View current data")
        print("2. Update income")
        print("3. Add expense")
        print("4. Save data")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_summary(income, expenses)

        elif choice == "2":
            income = get_number("Enter your total income for the month: $")

        elif choice == "3":
            expense = get_expense()

            if expense is not None:
                name, amount = expense

                if name in expenses:
                    expenses[name] += amount
                else:
                    expenses[name] = amount
        
        elif choice == "4":
            save_data(income, expenses)
            print("Data saved to finance_data.json")
        
        elif choice == "5": 
            save_data(income, expenses)
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, or 5.")
    print("=== Finance Tracker ===")

    
main()