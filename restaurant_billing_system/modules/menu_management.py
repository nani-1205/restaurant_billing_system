from database.database_manager import add_menu_item, get_menu_items
from models.menu_item import MenuItem
import logging

logging.basicConfig(level=logging.INFO)

def create_menu_item(name, category, price):
    try:
        add_menu_item(name, category, price)
        logging.info(f"Menu item '{name}' added successfully.")
    except Exception as e:
        logging.error(f"Error creating menu item: {e}")


def list_menu_items():
    items = get_menu_items()
    if not items:
        logging.info("No menu items found.")
        return []
    else:
        menu_items_list = []
        for item in items:
            menu_item = MenuItem(item[0], item[1], item[2], item[3])
            menu_items_list.append(str(menu_item))
        return menu_items_list