import json
import csv

def load_data():
    try:
        with open("finance_data.json", "r") as file:
            data = json.load(file)
            return data["income"], data["expenses"]
    except FileNotFoundError:
        return 0, {}
    
def save_data(income, expenses):
    data = {
        "income": income,
        "expenses": expenses
    }

    with open("finance_data.json", "w") as file:
        json.dump(data, file, indent=4)

def export_to_csv(income, expenses):
    with open("finance_data.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["type", "name", "amount"])
        writer.writeheader()
        writer.writerow({"type":"income", "name":"monthly income", "amount":income})
        for name, amount in expenses.items():
            writer.writerow({"type":"expenses", "name":name, "amount":amount})
        writer.writerow({"type":"summary", "name":"total expenses", "amount":sum(expenses.values())})
        writer.writerow({"type":"summary", "name":"balance", "amount": income - sum(expenses.values())})


def get_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid amount.")

def get_expense():
    while True: 
        name = input("Enter expense name: ").strip().lower()
        
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
        print("5. Export to csv")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_summary(income, expenses)

        elif choice == "2":
            income = get_number("Enter your total income for the month: $")

        elif choice == "3":
            name, amount = get_expense()

            if name in expenses:
                expenses[name] += amount
            else:
                expenses[name] = amount
        
        elif choice == "4":
            save_data(income, expenses)
            print("Data saved to finance_data.json")
        
        elif choice == "5":
            save_data(income, expenses)
            export_to_csv(income, expenses)
            print("Data exported to finance_data.csv")
        
        elif choice == "6": 
            save_data(income, expenses)
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")
    print("=== Finance Tracker ===")

    
if __name__ == "__main__":
    main()