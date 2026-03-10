def get_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid amount.")

def main():
    print("=== Finance Tracker ===")

    # 1) Ask for income 
    income = get_number("Enter your total income for the month: $")

    # 2) Ask for multiple expenses
    expenses = []

    while True:
        name = input("Enter expense name (or 'done' to finish): ")

        if name.lower() == "done":
            break

        amount = get_number(f"Enter amount for {name}: $")

        expenses.append((name, amount))
    
    # 3) Calculate balance (surplus/deficit)
    total_expenses = sum(amount for name, amount in expenses)
    balance = income - total_expenses

    print("\nExpenses:")
    for name, amount in expenses:
        print(f"{name}: ${amount:.2f}")

    print("\n--- Summary ---")
    print(f"Income: ${income:.2f}")
    print(f"Total expenses: ${total_expenses:.2f}")

    if balance > 0:
        print(f"Surplus: ${balance:.2f} ✅")
    elif balance < 0:
        print(f"Deficit: ${abs(balance):.2f}  ❌")
    else:
        print("Break-even: $0.00")
    
main()