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
        expense = get_number("Enter an expense amount (0 to finish): $")

        if expense == 0:
            break

        expenses.append(expense)
    
    # 3) Calculate balance (surplus/deficit)
    total_expenses = sum(expenses)
    balance = income - total_expenses

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