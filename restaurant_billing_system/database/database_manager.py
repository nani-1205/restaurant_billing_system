import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

DB_HOST = "your_mysql_host"  # Replace with your MySQL host
DB_USER = "your_mysql_user"  # Replace with your MySQL user
DB_PASSWORD = "your_mysql_password"  # Replace with your MySQL password
DB_NAME = "your_mysql_database"  # Replace with your MySQL database name

def get_connection():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

def create_tables():
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(255),
                price DECIMAL(10, 2) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tables (
                table_id INT PRIMARY KEY,
                status VARCHAR(255) DEFAULT 'available'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                table_id INT,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10, 2) DEFAULT 0.0,
                payment_method VARCHAR(255),
                FOREIGN KEY (table_id) REFERENCES tables(table_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                item_id INT,
                quantity INT DEFAULT 1,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
            )
        """)

        conn.commit()
        logging.info("Tables created successfully.")
    except mysql.connector.Error as e:
        logging.error(f"Error creating tables: {e}")
        if conn:
            conn.rollback()  # Rollback changes if an error occurs
    finally:
        if conn:
            conn.close()

def add_menu_item(name, category, price):
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO menu_items (name, category, price) VALUES (%s, %s, %s)", (name, category, price))
        conn.commit()
        logging.info(f"Menu item '{name}' added successfully.")
    except mysql.connector.Error as e:
        logging.error(f"Error adding menu item: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
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
    except mysql.connector.Error as e:
        logging.error(f"Error getting menu items: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_table_status(table_id):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT status FROM tables WHERE table_id = %s", (table_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as e:
        logging.error(f"Error getting table status: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_table_status(table_id, status):
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tables SET status = %s WHERE table_id = %s", (status, table_id))
        conn.commit()
        logging.info(f"Table {table_id} status updated to {status}.")
    except mysql.connector.Error as e:
        logging.error(f"Error updating table status: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def create_tables_db(num_tables):
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        for i in range(1, num_tables + 1):
            cursor.execute("INSERT INTO tables (table_id) VALUES (%s)", (i,))
        conn.commit()
        logging.info(f"{num_tables} tables created.")
    except mysql.connector.Error as e:
        logging.error(f"Error creating tables: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()