# main.py
import tkinter as tk
from gui.restaurant_app import RestaurantApp
from database.database_manager import create_tables
from modules.table_management import create_tables as create_table_module
import os

def main():
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_tables()  # Ensure tables are created on startup
    if not os.path.exists("restaurant.db"):
      create_table_module(5) # Create initial tables only if the db is new
    main()