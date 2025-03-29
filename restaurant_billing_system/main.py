from flask import Flask, render_template, request, redirect, url_for
from modules.menu_management import create_menu_item, list_menu_items
from modules.table_management import get_table_status, update_table_status, create_tables
from modules.order_taking import create_order, add_item_to_order, get_order_details, complete_order, calculate_order_total
from modules.billing import generate_bill, print_bill
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Saijagan@12'  # Replace with a strong secret key

if not os.path.exists("restaurant.db"):
    from database.database_manager import create_tables as create_db_tables
    create_db_tables()
    create_tables(5)

@app.route("/")
def index():
    tables = [i for i in range(1,6)]  #replace with actual table fetching logic if needed
    return render_template("index.html", tables=tables)

@app.route("/menu")
def menu():
    menu_items = list_menu_items()
    return render_template("menu.html", menu_items=menu_items)

@app.route("/add_menu_item", methods=['POST'])
def add_menu_item():
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    create_menu_item(name, category, price)
    return redirect(url_for('menu')) #Redirect to the menu page

@app.route("/table/<int:table_id>")
def table_details(table_id):
    status = get_table_status(table_id)
    return render_template("table_details.html", table_id = table_id, status = status)

#Add route for changing table status
@app.route("/update_table_status", methods=['POST'])
def update_table_status_route():
    table_id = int(request.form['table_id'])
    new_status = request.form['status']
    update_table_status(table_id, new_status)
    return redirect(url_for('table_details', table_id = table_id))


#Add order route and billing route.

if __name__ == "__main__":
    app.run(debug=True)