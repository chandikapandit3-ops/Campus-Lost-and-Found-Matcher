import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


def load_expenses():
    """Read all saved expenses from the CSV file."""
    expenses = []

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)

    except FileNotFoundError:
        # The file will be created when the first expense is added.
        pass

    return expenses


def save_expenses(expenses):
    """Save the complete expense list to the CSV file."""
    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for expense in expenses:
            writer.writerow(expense)


def get_amount():
    """Take a valid positive amount from the user."""
    while True:
        try:
            amount = float(input("Enter amount (₹): "))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def add_expense(expenses):
    """Add a new expense to the list."""
    print("\n--- Add Expense ---")

    category = input(
        "Enter category (Food/Travel/Study/Shopping/Other): "
    ).strip().title()

    description = input("Enter description: ").strip()
    amount = get_amount()

    date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully.")


def view_expenses(expenses):
    """Display all recorded expenses."""
    print("\n--- All Expenses ---")

    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    print("-" * 70)
    print(f"{'No.':<5}{'Date':<13}{'Category':<15}"
          f"{'Description':<22}{'Amount (₹)':>12}")
    print("-" * 70)

    for i, expense in enumerate(expenses, start=1):
        print(
            f"{i:<5}{expense['date']:<13}"
            f"{expense['category']:<15}"
            f"{expense['description'][:21]:<22}"
            f"{expense['amount']:>12.2f}"
        )

    print("-" * 70)


def total_expense(expenses):
    """Calculate total money spent."""
    return sum(expense["amount"] for expense in expenses)


def category_summary(expenses):
    """Calculate total spending for each category."""
    summary = {}

    for expense in expenses:
        category = expense["category"]

        if category not in summary:
            summary[category] = 0

        summary[category] += expense["amount"]

    return summary


def show_analysis(expenses):
    """Display spending analysis and identify the highest category."""
    print("\n--- Spending Analysis ---")

    if len(expenses) == 0:
        print("No expenses available for analysis.")
        return

    total = total_expense(expenses)
    summary = category_summary(expenses)

    print(f"Total Expense: ₹{total:.2f}")

    print("\nCategory-wise Spending:")

    # List comprehension is used to sort category totals.
    category_data = [
        (category, amount)
        for category, amount in summary.items()
    ]

    category_data.sort(key=lambda item: item[1], reverse=True)

    for category, amount in category_data:
        percentage = (amount / total) * 100
        print(f"{category:<15} ₹{amount:>10.2f}  ({percentage:.1f}%)")

    highest_category = category_data[0][0]
    highest_amount = category_data[0][1]

    print(
        f"\nHighest spending category: {highest_category} "
        f"(₹{highest_amount:.2f})"
    )


def budget_analysis(expenses):
    """Compare total spending with the user's budget."""
    print("\n--- Budget Analysis ---")

    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    while True:
        try:
            budget = float(input("Enter your budget (₹): "))

            if budget <= 0:
                print("Budget must be greater than 0.")
            else:
                break

        except ValueError:
            print("Invalid budget. Please enter a number.")

    total = total_expense(expenses)
    remaining = budget - total

    print(f"\nBudget: ₹{budget:.2f}")
    print(f"Total spent: ₹{total:.2f}")

    if remaining > 0:
        percentage_left = (remaining / budget) * 100

        print(f"Remaining budget: ₹{remaining:.2f}")
        print(f"Budget remaining: {percentage_left:.1f}%")

        if percentage_left <= 20:
            print("Alert: Your remaining budget is low.")
        else:
            print("Status: You are within your budget.")

    elif remaining == 0:
        print("Remaining budget: ₹0.00")
        print("Alert: You have exactly reached your budget.")

    else:
        overspent = abs(remaining)
        percentage_over = (overspent / budget) * 100

        print(f"Budget exceeded by: ₹{overspent:.2f}")
        print(f"Amount over budget: {percentage_over:.1f}%")
        print("Alert: You have exceeded your budget.")


def search_category(expenses):
    """Show expenses belonging to a selected category."""
    print("\n--- Search by Category ---")

    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    category = input("Enter category to search: ").strip().title()

    matches = [
        expense for expense in expenses
        if expense["category"] == category
    ]

    if len(matches) == 0:
        print("No expenses found in this category.")
        return

    print(f"\nExpenses in {category}:")

    for i, expense in enumerate(matches, start=1):
        print(
            f"{i}. {expense['date']} | "
            f"{expense['description']} | "
            f"₹{expense['amount']:.2f}"
        )

    category_total = sum(expense["amount"] for expense in matches)
    print(f"Total for {category}: ₹{category_total:.2f}")


def delete_expense(expenses):
    """Delete an expense selected by its number."""
    print("\n--- Delete Expense ---")

    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    view_expenses(expenses)

    while True:
        try:
            number = int(input("Enter expense number to delete: "))

            if 1 <= number <= len(expenses):
                removed = expenses.pop(number - 1)
                save_expenses(expenses)

                print(
                    f"Deleted: {removed['description']} "
                    f"(₹{removed['amount']:.2f})"
                )
                return

            print("Please enter a valid expense number.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("       STUDENT EXPENSE & BUDGET ANALYZER")
    print("=" * 50)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Spending Analysis")
    print("4. Budget Analysis")
    print("5. Search by Category")
    print("6. Delete Expense")
    print("7. Exit")
    print("=" * 50)


def main():
    """Run the complete project."""
    expenses = load_expenses()

    while True:
        show_menu()

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            show_analysis(expenses)

        elif choice == "4":
            budget_analysis(expenses)

        elif choice == "5":
            search_category(expenses)

        elif choice == "6":
            delete_expense(expenses)

        elif choice == "7":
            print("\nThank you for using Student Expense & Budget Analyzer.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
