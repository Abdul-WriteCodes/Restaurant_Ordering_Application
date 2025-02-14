import sqlite3
import uuid
from datetime import datetime

# Step 1: Connect to SQLite Database
def create_connection():
    conn = sqlite3.connect('restaurant_ordering.db')
    return conn

# Step 2: Create Database Schema
def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Create MenuItems table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MenuItems (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT
    )
    ''')

    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT,
        contact_info TEXT
    )
    ''')

    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        menu_item_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customers(id),
        FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id)
    )
    ''')

    conn.commit()
    conn.close()

# Step 3: Populate Sample Data (only once)
def populate_sample_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Check if there are any entries in the MenuItems table
    cursor.execute('SELECT * FROM MenuItems LIMIT 1')
    existing_item = cursor.fetchone()

    if existing_item is None:  # Only insert if no menu items are present
        menu_items = [
            ('Burger', 5.99, 'A delicious beef burger'),
            ('Pizza', 8.99, 'Cheesy pepperoni pizza'),
            ('Salad', 4.99, 'Fresh garden salad')
        ]

        for item in menu_items:
            cursor.execute('INSERT INTO MenuItems (name, price, description) VALUES (?, ?, ?)', item)

    conn.commit()
    conn.close()

# Step 4: Database Operations
def view_menu():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM MenuItems')
    items = cursor.fetchall()
    conn.close()
    return items

def place_order(customer_id, menu_items):
    conn = create_connection()
    cursor = conn.cursor()

    total_price = 0
    order_details = []

    for menu_item_id, quantity in menu_items:
        cursor.execute('''
        INSERT INTO Orders (customer_id, menu_item_id, quantity, order_date)
        VALUES (?, ?, ?, datetime('now'))
        ''', (customer_id, menu_item_id, quantity))

        cursor.execute('SELECT name, price FROM MenuItems WHERE id = ?', (menu_item_id,))
        item_details = cursor.fetchone()

        # Store item details (name, quantity, price) for invoice generation
        order_details.append((item_details[0], quantity, item_details[1]))

        total_price += item_details[1] * quantity

    conn.commit()
    conn.close()

    return total_price, order_details

def retrieve_orders():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Orders')
    orders = cursor.fetchall()
    conn.close()
    return orders

# Step 5: Generate Invoice
def generate_invoice(customer, order_items, total_price):
    invoice_reference = str(uuid.uuid4())
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    print("\n--- Order Invoice ---")
    print(f"Invoice Reference: {invoice_reference}")
    print(f"Date and Time: {timestamp}")
    print(f"Customer Name: {customer[1]}")
    print(f"Customer Address: {customer[2]}")
    print(f"Customer Contact Number: {customer[3]}")
    print("\nOrdered Items:")

    for item in order_items:
        print(f"{item[0]} (x{item[1]}) - ${item[2]:.2f} each")

    print(f"\nNet Total: ${total_price:.2f}")
    print("\n--- Thank you for your order! ---")

# Step 6: Command-line Interface (CLI)
def main():
    initialize_database()  # Run this once to set up the database
    populate_sample_data()  # Run this once to populate sample data

    while True:
        print("\n--- Restaurant Ordering System ---")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View Placed Orders")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            menu = view_menu()
            print("\nMenu Items:")
            for item in menu:
                print(f"ID: {item[0]} |Name: {item[1]}| Price: ${item[2]:.2f} |Description: {item[3]}")

        elif choice == '2':
            customer_name = input("Enter your name: ")
            customer_address = input("Enter your address: ")
            customer_contact = input("Enter your contact number: ")

            # Add customer to the database
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Customers (name, address, contact_info) 
            VALUES (?, ?, ?)
            ''', (customer_name, customer_address, customer_contact))
            customer_id = cursor.lastrowid
            conn.commit()

            # Place the order
            menu = view_menu()
            print("\nSelect items (enter item ID and quantity). Type 'done' when finished.")
            order_items = []
            while True:
                item_id = input("Enter item ID: ")
                if item_id.lower() == 'done':
                    break
                item_id = int(item_id)
                quantity = int(input(f"Enter quantity for item {item_id}: "))
                order_items.append((item_id, quantity))

            total_price, order_details = place_order(customer_id, order_items)
            payment = float(input(f"Enter payment amount: ${total_price:.2f}: "))
            if payment >= total_price:
                print("Payment successful!")
                generate_invoice((customer_id, customer_name, customer_address, customer_contact), order_details, total_price)
            else:
                print("Insufficient payment. Order canceled.")

        elif choice == '3':
            orders = retrieve_orders()
            print("\nOrders:")
            for order in orders:
                print(order)

        elif choice == '4':
            print("Thank you for using the Restaurant Ordering System!")
            break

if __name__ == "__main__":
    main()
