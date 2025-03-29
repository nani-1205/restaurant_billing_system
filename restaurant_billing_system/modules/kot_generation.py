from modules.order_taking import get_order_details
from modules.table_management import get_table_status
import datetime
import logging
from escpos.printer import Serial  # Or Usb, Network, etc.

logging.basicConfig(level=logging.INFO)

def generate_kot(order_id, table_id):
    try:
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
    except Exception as e:
        logging.error(f"Error generating KOT: {e}")
        return None

def print_kot(kot_text):
    try:
        # Adjust these settings to match your printer
        p = Serial(devfile='/dev/ttyUSB1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.0) #Different location than before
        p.text(kot_text)
        p.cut()  # Cut the paper
        p.close()
        logging.info("KOT printed successfully.")
    except Exception as e:
        logging.error(f"Error printing KOT: {e}")