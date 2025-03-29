from modules.order_taking import get_order_details
from modules.table_management import get_table_status
import datetime

def generate_kot(order_id, table_id):
    order_details = get_order_details(order_id)
    table_status = get_table_status(table_id)

    kot = f"""
    Kitchen Order Ticket (KOT)
    Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Table: {table_id} ({table_status})
    Order ID: {order_id}

    Items:
    """
    for item_name, item_price, item_quantity in order_details:
        kot += f"- {item_name} x {item_quantity}\n"

    kot += "---------------------------------"

    return kot

def print_kot(kot_text):
    print(kot_text)  # Replace with actual printing logic