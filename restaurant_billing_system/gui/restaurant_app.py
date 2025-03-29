import tkinter as tk
from tkinter import ttk
from modules.menu_management import create_menu_item, list_menu_items
from modules.table_management import get_table_status, update_table_status

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Billing System")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Table Management Tab
        self.table_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.table_tab, text="Table Management")
        self.create_table_management_ui(self.table_tab)

        # Menu Management Tab
        self.menu_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.menu_tab, text="Menu Management")
        self.create_menu_management_ui(self.menu_tab)

    def create_table_management_ui(self, tab):
        #Table ID Label and Input
        table_id_label = ttk.Label(tab, text="Table ID:")
        table_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.table_id_entry = ttk.Entry(tab)
        self.table_id_entry.grid(row=0, column=1, padx=5, pady=5)

        #Status Label
        status_label = ttk.Label(tab, text="Table Status: ")
        status_label.grid(row=1, column=0, padx=5, pady=5)
        self.status_display = tk.StringVar()
        self.status_display.set("Available")
        status_value_label = ttk.Label(tab, textvariable=self.status_display)
        status_value_label.grid(row=1, column=1, padx=5, pady=5)

        #Get Status Button
        get_status_button = ttk.Button(tab, text="Get Status", command=self.get_table_status_gui)
        get_status_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        #Update Status
        status_update_label = ttk.Label(tab, text="Update Status:")
        status_update_label.grid(row=3, column=0, padx=5, pady=5)

        self.status_combobox = ttk.Combobox(tab, values=["available", "occupied", "reserved"])
        self.status_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.status_combobox.set("available")

        update_status_button = ttk.Button(tab, text="Update", command=self.update_table_status_gui)
        update_status_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def get_table_status_gui(self):
        table_id = self.table_id_entry.get()
        if not table_id.isdigit():
            self.status_display.set("Invalid Table ID")
            return

        status = get_table_status(int(table_id))
        if status:
            self.status_display.set(status)
        else:
            self.status_display.set("Table not found")

    def update_table_status_gui(self):
        table_id = self.table_id_entry.get()
        new_status = self.status_combobox.get()

        if not table_id.isdigit():
            self.status_display.set("Invalid Table ID")
            return

        update_table_status(int(table_id), new_status)
        self.get_table_status_gui() #Refresh status

    def create_menu_management_ui(self, tab):
        # Item Name
        item_name_label = ttk.Label(tab, text="Item Name:")
        item_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.item_name_entry = ttk.Entry(tab)
        self.item_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category
        category_label = ttk.Label(tab, text="Category:")
        category_label.grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(tab)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        # Price
        price_label = ttk.Label(tab, text="Price:")
        price_label.grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(tab)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        # Add Button
        add_button = ttk.Button(tab, text="Add Item", command=self.add_menu_item_gui)
        add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # List Items Button
        list_button = ttk.Button(tab, text="List Items", command=self.list_menu_items_gui)
        list_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Text area to display menu items
        self.menu_text_area = tk.Text(tab, height=10, width=40)
        self.menu_text_area.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def add_menu_item_gui(self):
        name = self.item_name_entry.get()
        category = self.category_entry.get()
        price_str = self.price_entry.get()

        if not name or not category or not price_str:
            self.menu_text_area.insert(tk.END, "Please fill all fields.\n")
            return

        try:
            price = float(price_str)
            create_menu_item(name, category, price)
            self.menu_text_area.insert(tk.END, f"Added {name} to menu.\n")
        except ValueError:
            self.menu_text_area.insert(tk.END, "Invalid price format.\n")

    def list_menu_items_gui(self):
         self.menu_text_area.delete("1.0", tk.END) #Clear text area
         items = list_menu_items() #Gets items from db
         if not items:
             self.menu_text_area.insert(tk.END, "No menu items found.\n")
         else:
             for item in items:
                self.menu_text_area.insert(tk.END, f"{item}\n") #Assumes that the list_menu_items returns a list of strings