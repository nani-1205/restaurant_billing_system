import sqlite3

DATABASE_NAME = "restaurant.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tables (
            table_id INTEGER PRIMARY KEY,
            status TEXT DEFAULT 'available'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL DEFAULT 0.0,
            payment_method TEXT,
            FOREIGN KEY (table_id) REFERENCES tables(table_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
        )
    """)

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

#Example functions to add, update and retrieve data
def add_menu_item(name, category, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)", (name, category, price))
    conn.commit()
    conn.close()

def get_menu_items():
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM menu_items")
     items = cursor.fetchall()
     conn.close()
     return items

def get_table_status(table_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM tables WHERE table_id = ?", (table_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def update_table_status(table_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tables SET status = ? WHERE table_id = ?", (status, table_id))
    conn.commit()
    conn.close()
    print(f"Table {table_id} status updated to {status}.")

def create_tables_db(num_tables):
    conn = get_connection()
    cursor = conn.cursor()
    for i in range(1, num_tables + 1):
      cursor.execute("INSERT INTO tables (table_id) VALUES (?)", (i,))
    conn.commit()
    conn.close()
    print(f"{num_tables} tables created.")

# models/__init__.py
# (This file can be empty)

# models/menu_item.py
class MenuItem:
    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.category}): ${self.price:.2f}"

# modules/__init__.py
# (This file can be empty)

# modules/menu_management.py
from database.database_manager import add_menu_item, get_menu_items
from models.menu_item import MenuItem

def create_menu_item(name, category, price):
    add_menu_item(name, category, price)
    print(f"Menu item '{name}' added successfully.")

def list_menu_items():
    items = get_menu_items()
    if not items:
        print("No menu items found.")
    else:
        menu_items = []
        for item in items:
            menu_item = MenuItem(item[0], item[1], item[2], item[3])
            menu_items.append(str(menu_item))
        return menu_items