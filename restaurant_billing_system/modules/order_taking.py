from database.database_manager import get_connection # add other imports as needed

def create_order(table_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (table_id) VALUES (?)", (table_id,))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def add_item_to_order(order_id, item_id, quantity=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))
    conn.commit()
    conn.close()
    print(f"Item {item_id} added to order {order_id}.")

def get_order_details(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mi.name, mi.price, oi.quantity
        FROM order_items oi
        JOIN menu_items mi ON oi.item_id = mi.item_id
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def calculate_order_total(order_id):
    order_items = get_order_details(order_id)
    total = sum(item[1] * item[2] for item in order_items) #price * quantity
    return total

def update_order_total(order_id, total):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (total, order_id))
    conn.commit()
    conn.close()

def complete_order(order_id, payment_method):
    total = calculate_order_total(order_id)
    update_order_total(order_id, total)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET payment_method = ? WHERE order_id = ?", (payment_method, order_id))
    conn.commit()
    conn.close()
    print(f"Order {order_id} completed with payment method: {payment_method}, Total: ${total:.2f}")
    return total