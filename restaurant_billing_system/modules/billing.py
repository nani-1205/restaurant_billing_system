from modules.order_taking import get_order_details, calculate_order_total, complete_order
import datetime
import logging
from escpos.printer import Serial  # Or Usb, Network, etc.

logging.basicConfig(level=logging.INFO)

def generate_bill(order_id, discount_percent=0, discount_amount=0):
    order_details = get_order_details(order_id)
    total_amount = calculate_order_total(order_id)

    if discount_percent:
        discount = (discount_percent / 100) * total_amount
    elif discount_amount:
        discount = discount_amount
    else:
        discount = 0

    final_amount = total_amount - discount

    bill = f"""
    Restaurant Bill
    Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Order ID: {order_id}

    Items:
    """
    for item_name, item_price, item_quantity in order_details:
        bill += f"- {item_name} x {item_quantity}: ${item_price * item_quantity:.2f}\n"

    bill += f"""
    ---------------------------------
    Subtotal: ${total_amount:.2f}
    Discount: ${discount:.2f}
    Total: ${final_amount:.2f}
    ---------------------------------
    Thank you for your visit!
    """

    return bill

def print_bill(bill_text):
    try:
        # Adjust these settings to match your printer
        p = Serial(devfile='/dev/ttyUSB0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.0)
        p.text(bill_text)
        p.cut()  # Cut the paper
        p.close()
        logging.info("Receipt printed successfully.")
    except Exception as e:
        logging.error(f"Error printing receipt: {e}")