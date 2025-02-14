# Restaurant_Ordering_Application
This is a simple restaurant ordering system prototype built using Python and SQLite3. The application allows users to view a menu, place orders, and generate invoices. It stores all data, including customer information, menu items, and orders, in an SQLite database for efficient management.

## Features

- **Menu Management:** Displays available menu items with details (name, price, description).
- **Order Placement:** Allows customers to place orders with specified quantities.
- **Invoice Generation:** After payment, an invoice with order details and total price is generated.
- **Order Management:** Ability to view all placed orders.
- **Database Management:** Uses SQLite3 to manage the database and store data.

## Requirements

- Python 3.x
- SQLite3 (comes bundled with Python)

## Installation

1. **Clone the repository** or download the script files.

2. **Install Python** (if not already installed). You can download Python from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/).

3. **Run the script:**
   - Open a terminal or command prompt.
   - Navigate to the folder containing the script.
   - Run the script using:
     ```
     python restaurant_ordering_system.py
     ```

## Usage

### Step 1: Initialize the Database
The first time you run the program, it will automatically create an SQLite3 database file (`restaurant_ordering.db`) and initialize necessary tables: `MenuItems`, `Customers`, and `Orders`.

### Step 2: Populate Sample Data
Sample menu items will be populated in the `MenuItems` table automatically if there are no items present.

### Step 3: Command-Line Interface (CLI)
Once the application is running, you’ll be presented with a menu of options:

1. **View Menu:** Displays all available menu items.
2. **Place Order:** Enter customer details (name, address, contact info) and select items from the menu to order. After completing the order, enter payment information to generate an invoice.
3. **View Placed Orders:** Displays all orders placed in the system.
4. **Exit:** Closes the program.

### Step 4: Invoice Generation
Once a customer’s payment is successful, an invoice will be generated, showing order details such as:
- Invoice reference number
- Date and time of the order
- Customer’s name, address, and contact number
- Ordered items with quantities and prices
- Total order price

## Example Workflow

1. **Start the program** and choose **1** to view the menu.
2. **Place an order** by entering your details and selecting items.
3. After placing an order, make the **payment**, and an invoice will be printed with the details of your order.

## Database Structure

### MenuItems Table
- **id** (INTEGER, Primary Key)
- **name** (TEXT)
- **price** (REAL)
- **description** (TEXT)

### Customers Table
- **id** (INTEGER, Primary Key)
- **name** (TEXT)
- **address** (TEXT)
- **contact_info** (TEXT)

### Orders Table
- **id** (INTEGER, Primary Key)
- **customer_id** (INTEGER, Foreign Key referencing Customers.id)
- **menu_item_id** (INTEGER, Foreign Key referencing MenuItems.id)
- **quantity** (INTEGER)
- **order_date** (TEXT)

## Contributing

Feel free to fork this project, submit issues, and send pull requests. Improvements and suggestions are welcome!

## License

This project is open-source and available under the [MIT License](LICENSE).
