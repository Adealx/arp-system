import json
import os

customers = []

FILE_NAME = "customers.json"


def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(customers, file)


def load_data():
    global customers

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            customers = json.load(file)


def add_customer(name, invoice, paid):
    balance = invoice - paid

    customer = {
        "name": name,
        "invoice": invoice,
        "paid": paid,
        "balance": balance
    }

    customers.append(customer)
    save_data()
    print("Customer added successfully")


def view_customers():
    print("\n--- CUSTOMER REPORT ---")

    for customer in customers:
        print(customer["name"], "- Balance:", customer["balance"])


def total_outstanding():
    total = 0

    for customer in customers:
        total += customer["balance"]

    print("Total Outstanding Debt:", total)


def delete_customer(name):
    for customer in customers:
        if customer["name"] == name:
            customers.remove(customer)
            save_data()
            print("Customer deleted successfully")
            return

    print("Customer not found")


def update_invoice(name, new_invoice):
    for customer in customers:
        if customer["name"] == name:
            customer["invoice"] = new_invoice
            customer["balance"] = new_invoice - customer["paid"]
            save_data()
            print("Invoice updated successfully")
            return

    print("Customer not found")


load_data()

while True:
    print("\nARP SYSTEM")
    print("1. Add Customer")
    print("2. View Customers")
    print("3. Total Debt")
    print("4. Delete Customer")
    print("5. Update Invoice")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Customer name: ")
        invoice = int(input("Invoice amount: "))
        paid = int(input("Amount paid: "))
        add_customer(name, invoice, paid)

    elif choice == "2":
        view_customers()

    elif choice == "3":
        total_outstanding()

    elif choice == "4":
        name = input("Enter customer name to delete: ")
        delete_customer(name)

    elif choice == "5":
        name = input("Customer name: ")
        new_invoice = int(input("New invoice amount: "))
        update_invoice(name, new_invoice)

    elif choice == "6":
        print("Exiting system...")
        break

    else:
        print("Invalid choice")