from database.database_manager import get_connection
import logging

logging.basicConfig(level=logging.INFO)

def create_order(table_id):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders (table_id) VALUES (?)", (table_id,))
        order_id = cursor.lastrowid
        conn.commit()
        logging.info(f"Created order {order_id} for table {table_id}")
        return order_id
    except Exception as e:
        logging.error(f"Error creating order for table {table_id}: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def add_item_to_order(order_id, item_id, quantity=1):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))
        conn.commit()
        logging.info(f"Added item {item_id} to order {order_id} with quantity {quantity}")
        return True
    except Exception as e:
        logging.error(f"Error adding item {item_id} to order {order_id}: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def get_order_details(order_id):
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT mi.name, mi.price, oi.quantity
            FROM order_items oi
            JOIN menu_items mi ON oi.item_id = mi.item_id
            WHERE oi.order_id = ?
        """, (order_id,))
        items = cursor.fetchall()
        return items
    except Exception as e:
        logging.error(f"Error getting order details for order {order_id}: {e}")
        return []
    finally:
        if conn:
            conn.close()

def calculate_order_total(order_id):
    order_items = get_order_details(order_id)
    total = sum(item[1] * item[2] for item in order_items)  # price * quantity
    return total

def update_order_total(order_id, total):
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (total, order_id))
        conn.commit()
        logging.info(f"Updated order {order_id} total to {total}")
        return True
    except Exception as e:
        logging.error(f"Error updating order {order_id} total: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def complete_order(order_id, payment_method):
    total = calculate_order_total(order_id)
    if not update_order_total(order_id, total):
        return False

    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET payment_method = ? WHERE order_id = ?", (payment_method, order_id))
        conn.commit()
        logging.info(f"Order {order_id} completed with payment method {payment_method}, Total: {total}")
        return total
    except Exception as e:
        logging.error(f"Error completing order {order_id}: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()