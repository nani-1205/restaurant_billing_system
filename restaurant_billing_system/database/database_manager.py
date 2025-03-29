import sqlite3
import logging

DATABASE_NAME = "restaurant.db"
logging.basicConfig(level=logging.INFO)

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

def create_tables():
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
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
        logging.info("Tables created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error creating tables: {e}")
        conn.rollback()  # Rollback changes if an error occurs
    finally:
        conn.close()

def add_menu_item(name, category, price):
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)", (name, category, price))
        conn.commit()
        logging.info(f"Menu item '{name}' added successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error adding menu item: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_menu_items():
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM menu_items")
        items = cursor.fetchall()
        return items
    except sqlite3.Error as e:
        logging.error(f"Error getting menu items: {e}")
        return []
    finally:
        conn.close()

def get_table_status(table_id):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM tables WHERE table_id = ?", (table_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        logging.error(f"Error getting table status: {e}")
        return None
    finally:
        conn.close()

def update_table_status(table_id, status):
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tables SET status = ? WHERE table_id = ?", (status, table_id))
        conn.commit()
        logging.info(f"Table {table_id} status updated to {status}.")
    except sqlite3.Error as e:
        logging.error(f"Error updating table status: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_tables_db(num_tables):
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        for i in range(1, num_tables + 1):
            cursor.execute("INSERT INTO tables (table_id) VALUES (?)", (i,))
        conn.commit()
        logging.info(f"{num_tables} tables created.")
    except sqlite3.Error as e:
        logging.error(f"Error creating tables: {e}")
        if conn:
            conn.rollback()
    finally:
        conn.close()