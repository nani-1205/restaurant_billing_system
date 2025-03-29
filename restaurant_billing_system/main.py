from flask import Flask, render_template, request, redirect, url_for
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

# LOAD MODULES WITH TRY EXCEPT BLOCKS TO SEE ERRORS
try:
    from modules.menu_management import create_menu_item, list_menu_items
    logging.info("Menu management loaded successfully.")
except Exception as e:
    logging.exception("Error loading menu management module.")

try:
    from modules.table_management import get_table_status, update_table_status, create_tables
    logging.info("Table management loaded successfully.")
except Exception as e:
    logging.exception("Error loading table management module.")

try:
    from modules.order_taking import create_order, add_item_to_order, get_order_details, complete_order, calculate_order_total
    logging.info("Order taking loaded successfully.")
except Exception as e:
    logging.exception("Error loading order taking module.")

try:
    from modules.billing import generate_bill, print_bill
    logging.info("Billing loaded successfully.")
except Exception as e:
    logging.exception("Error loading billing module.")

try:
    from database.database_manager import create_tables as create_db_tables
    if not os.path.exists("restaurant.db"):
        create_db_tables()
        create_tables(5)
        logging.info("Database initialized.")
except Exception as e:
    logging.exception("Error initializing database.")
## THE MAIN ROUTES AND ERROR MESSAGING

@app.route("/")
def index():
    try:
        tables = [i for i in range(1,6)]  #replace with actual table fetching logic if needed
        return render_template("index.html", tables=tables)
    except Exception as e:
        logging.exception("Error rendering index page.")
        return "An error occurred.", 500 #Internal Server Error

@app.route("/menu")
def menu():
    try:
        menu_items = list_menu_items()
        return render_template("menu.html", menu_items=menu_items)
    except Exception as e:
        logging.exception("Error rendering menu page.")
        return "An error occurred.", 500

@app.route("/add_menu_item", methods=['POST'])
def add_menu_item():
    try:
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        create_menu_item(name, category, price)
        return redirect(url_for('menu')) #Redirect to the menu page
    except Exception as e:
        logging.exception("Error adding menu item.")
        return "An error occurred.", 500

@app.route("/table/<int:table_id>")
def table_details(table_id):
    try:
        status = get_table_status(table_id)
        return render_template("table_details.html", table_id = table_id, status = status)
    except Exception as e:
        logging.exception(f"Error rendering table details for table {table_id}.")
        return "An error occurred.", 500

#Add route for changing table status
@app.route("/update_table_status", methods=['POST'])
def update_table_status_route():
    try:
        table_id = int(request.form['table_id'])
        new_status = request.form['status']
        update_table_status(table_id, new_status)
        return redirect(url_for('table_details', table_id = table_id))
    except Exception as e:
        logging.exception("Error updating table status.")
        return "An error occurred.", 500

#Add order route and billing route.

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)