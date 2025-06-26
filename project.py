import csv
import os
from datetime import datetime
from typing import List, Dict, Tuple


def main():
    """Main function to run the personal finance tracker."""
    print("Welcome to Personal Finance Tracker!")
    
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View All Transactions")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            add_transaction("income")
        elif choice == "2":
            add_transaction("expense")
        elif choice == "3":
            display_summary()
        elif choice == "4":
            display_all_transactions()
        elif choice == "5":
            print("Thank you for using Personal Finance Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")


def add_transaction(transaction_type: str) -> bool:
    """
    Add a new transaction (income or expense) to the CSV file.
    
    Args:
        transaction_type (str): Either "income" or "expense"
    
    Returns:
        bool: True if transaction was added successfully, False otherwise
    """
    try:
        amount = float(input(f"Enter {transaction_type} amount: $"))
        if amount <= 0:
            print("Amount must be positive!")
            return False
        
        description = input(f"Enter {transaction_type} description: ").strip()
        if not description:
            print("Description cannot be empty!")
            return False
        
        category = input(f"Enter {transaction_type} category: ").strip()
        if not category:
            print("Category cannot be empty!")
            return False
        
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Create transactions.csv if it doesn't exist
        file_exists = os.path.exists("transactions.csv")
        
        with open("transactions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(["Date", "Type", "Amount", "Description", "Category"])
            
            writer.writerow([date, transaction_type, amount, description, category])
        
        print(f"{transaction_type.capitalize()} of ${amount:.2f} added successfully!")
        return True
        
    except ValueError:
        print("Invalid amount entered!")
        return False
    except Exception as e:
        print(f"Error adding transaction: {e}")
        return False


def calculate_balance() -> Tuple[float, float, float]:
    """
    Calculate total income, expenses, and balance from transactions.
    
    Returns:
        Tuple[float, float, float]: (total_income, total_expenses, balance)
    """
    total_income = 0.0
    total_expenses = 0.0
    
    try:
        if not os.path.exists("transactions.csv"):
            return (0.0, 0.0, 0.0)
        
        with open("transactions.csv", "r") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                amount = float(row["Amount"])
                if row["Type"] == "income":
                    total_income += amount
                elif row["Type"] == "expense":
                    total_expenses += amount
    
    except Exception as e:
        print(f"Error calculating balance: {e}")
        return (0.0, 0.0, 0.0)
    
    balance = total_income - total_expenses
    return (total_income, total_expenses, balance)


def get_category_breakdown() -> Dict[str, Dict[str, float]]:
    """
    Get breakdown of income and expenses by category.
    
    Returns:
        Dict[str, Dict[str, float]]: Nested dict with income/expense categories and amounts
    """
    breakdown = {"income": {}, "expense": {}}
    
    try:
        if not os.path.exists("transactions.csv"):
            return breakdown
        
        with open("transactions.csv", "r") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                transaction_type = row["Type"]
                category = row["Category"]
                amount = float(row["Amount"])
                
                if category in breakdown[transaction_type]:
                    breakdown[transaction_type][category] += amount
                else:
                    breakdown[transaction_type][category] = amount
    
    except Exception as e:
        print(f"Error getting category breakdown: {e}")
    
    return breakdown


def display_summary():
    """Display financial summary including balance and category breakdown."""
    total_income, total_expenses, balance = calculate_balance()
    
    print("\n--- Financial Summary ---")
    print(f"Total Income:  ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Balance:       ${balance:.2f}")
    
    if balance >= 0:
        print("✓ You're in the positive!")
    else:
        print("⚠ You're spending more than you earn!")
    
    # Category breakdown
    breakdown = get_category_breakdown()
    
    if breakdown["income"]:
        print("\n--- Income by Category ---")
        for category, amount in breakdown["income"].items():
            print(f"{category}: ${amount:.2f}")
    
    if breakdown["expense"]:
        print("\n--- Expenses by Category ---")
        for category, amount in breakdown["expense"].items():
            print(f"{category}: ${amount:.2f}")


def display_all_transactions():
    """Display all transactions from the CSV file."""
    try:
        if not os.path.exists("transactions.csv"):
            print("No transactions found.")
            return
        
        with open("transactions.csv", "r") as file:
            reader = csv.DictReader(file)
            transactions = list(reader)
            
            if not transactions:
                print("No transactions found.")
                return
            
            print("\n--- All Transactions ---")
            print(f"{'Date':<12} {'Type':<8} {'Amount':<10} {'Category':<15} {'Description'}")
            print("-" * 70)
            
            for row in transactions:
                amount_str = f"${float(row['Amount']):.2f}"
                print(f"{row['Date']:<12} {row['Type']:<8} {amount_str:<10} {row['Category']:<15} {row['Description']}")
    
    except Exception as e:
        print(f"Error displaying transactions: {e}")


if __name__ == "__main__":
    main()
