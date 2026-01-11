# Company Account & Warehouse with Save/Load
# Name: Your Name
# Student Number: XXXXX

import os
from ast import literal_eval

# Filenames for persistence
BALANCE_FILE = "account_balance.txt"
WAREHOUSE_FILE = "warehouse.txt"
HISTORY_FILE = "operations_history.txt"

def load_file(filename, default):
    """Load data from file, return default if error occurs"""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = f.read()
                return literal_eval(data)
        except Exception as e:
            print(f"Warning: Could not read {filename}. Starting fresh. ({e})")
    return default

def save_file(filename, data):
    """Save data to file"""
    try:
        with open(filename, "w") as f:
            f.write(repr(data))
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def show_commands():
    print("\nAvailable commands:")
    print("balance, sale, purchase, account, list, warehouse, review, end\n")

def main():
    # Load data or initialize defaults
    account = load_file(BALANCE_FILE, 0.0)
    warehouse = load_file(WAREHOUSE_FILE, {})
    operations = load_file(HISTORY_FILE, [])

    show_commands()

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "end":
            # Save data before exit
            save_file(BALANCE_FILE, account)
            save_file(WAREHOUSE_FILE, warehouse)
            save_file(HISTORY_FILE, operations)
            print("Data saved. Exiting program. Goodbye!")
            break

        elif command == "balance":
            try:
                amt = float(input("Enter amount to add (+) or subtract (-): "))
                account += amt
                operations.append(f"Balance change: {amt:.2f}, New balance: {account:.2f}")
                print(f"Updated account balance: {account:.2f}")
            except ValueError:
                print("Invalid number.")

        elif command == "sale":
            product = input("Product name: ").strip()
            try:
                price = float(input("Sale price: "))
                qty = int(input("Quantity sold: "))
                if product not in warehouse or warehouse[product]["quantity"] < qty:
                    print(f"Not enough '{product}' in warehouse.")
                    continue
                warehouse[product]["quantity"] -= qty
                account += price * qty
                operations.append(f"Sale: {qty} x {product} at {price:.2f}, New balance: {account:.2f}")
                print(f"Sale recorded. Account balance: {account:.2f}")
            except ValueError:
                print("Invalid input.")

        elif command == "purchase":
            product = input("Product name: ").strip()
            try:
                price = float(input("Purchase price: "))
                qty = int(input("Quantity purchased: "))
                total = price * qty
                if total > account:
                    print("Not enough balance for this purchase.")
                    continue
                if product in warehouse:
                    warehouse[product]["quantity"] += qty
                    warehouse[product]["price"] = price
                else:
                    warehouse[product] = {"price": price, "quantity": qty}
                account -= total
                operations.append(f"Purchase: {qty} x {product} at {price:.2f}, New balance: {account:.2f}")
                print(f"Purchase recorded. Account balance: {account:.2f}")
            except ValueError:
                print("Invalid input.")

        elif command == "account":
            print(f"Current account balance: {account:.2f}")

        elif command == "list":
            if not warehouse:
                print("Warehouse is empty.")
            else:
                print("\nWarehouse Inventory:")
                print(f"{'Product':15} {'Price':>10} {'Quantity':>10}")
                for prod, info in warehouse.items():
                    print(f"{prod:15} {info['price']:>10.2f} {info['quantity']:>10}")

        elif command == "warehouse":
            product = input("Enter product name: ").strip()
            if product in warehouse:
                info = warehouse[product]
                print(f"{product}: Price = {info['price']:.2f}, Quantity = {info['quantity']}")
            else:
                print(f"{product} not found.")

        elif command == "review":
            from_idx = input("From index (empty for 0): ").strip()
            to_idx = input("To index (empty for end): ").strip()
            try:
                start = int(from_idx) if from_idx else 0
                end = int(to_idx) if to_idx else len(operations)
                if start < 0 or end > len(operations) or start > end:
                    print("Invalid indices.")
                    continue
                print("\nRecorded operations:")
                for i in range(start, end):
                    print(f"{i}: {operations[i]}")
            except ValueError:
                print("Indices must be integers.")

        else:
            print("Invalid command. Please choose a valid option.")

        show_commands()


if __name__ == "__main__":
    main()
