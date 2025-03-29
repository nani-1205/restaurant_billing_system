from database.database_manager import get_connection  # add other imports as needed
import logging

logging.basicConfig(level=logging.INFO)

def create_order(table_id):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders (table_id) VALUES (%s)", (table_id,))
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

# (Other functions like add_item_to_order, get_order_details, etc. follow the same pattern)