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

    # 2) Ask for expenses
    expenses = get_number("Enter your total expenses for the month: $")
    
    # 3) Calculate balance (surplus/deficit)
    balance = income - expenses

    print("\n--- Summary ---")
    print(f"Income: ${income:.2f}")
    print(f"Expenses: ${expenses:.2f}")

    if balance > 0:
        print(f"Surplus: ${balance:.2f} ✅")
    elif balance < 0:
        print(f"Deficit: ${abs(balance):.2f}  ❌")
    else:
        print("Break-even: $0.00")
    
main()