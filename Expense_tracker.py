from Expenses import Expense
import calendar
import datetime


def main():
    print(f"Running Expense Tracker!!!")
    expense_file_path = "expenses.csv"
    budget = 5000

    #get user input for expense.
    expense = get_user_expense()

    #Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    #read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print(f"🎯Getting User Expense💸")
    expense_name = input("Enter Expense Name: ")
    expense_amount = float(input("Enter Expense Amount: "))
    expense_categories = [
        "🍕Food",
        "🏠Home",
        "💼Work",
        "🎉Fun",
        "✨Misc"
    ]
    while True:
        print("Select a Category:")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input(f"Select Category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid Category. Please Try Again.")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯Saving User Expense💸: {expense} to {expense_file_path}" )
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"🎯Summarizing Expenses💸")
    expenses = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            expense_name, expense_category, expense_amount = stripped_line.split(",")
            expense_amount = float(expense_amount)  # 🔧 FIXED HERE
            print(expense_name, expense_amount, expense_category)
            line_expense = Expense(
                name=expense_name, category=expense_category, amount=expense_amount
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("\n📊 Total by Category:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    # ✅ Now do the summary after the loop
    total_spent = sum([expense.amount for expense in expenses])
    print(red(f"\n💵 You've Spent a Total of: ${total_spent:.2f} This Month"))

    remaining_budget = budget - total_spent
    print(blue(f"✅ Remaining Budget: ${remaining_budget:.2f}"))

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉Budget pey day: ${daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"
def blue(text):
    return f"\033[94m{text}\033[0m"
def red(text):
    return f"\033[91m{text}\033[0m"



if __name__ == "__main__":
    main()