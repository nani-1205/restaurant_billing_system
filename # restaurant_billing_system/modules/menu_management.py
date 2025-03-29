# Requires database.py
from database import add_menu_item, get_menu_items

class MenuItem:
    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price

    def __str__(self):
        return f"{self.name} ({self.category}): ${self.price:.2f}"



def create_menu_item(name, category, price):
    add_menu_item(name, category, price)
    print(f"Menu item '{name}' added successfully.")

def list_menu_items():
    items = get_menu_items()
    if not items:
        print("No menu items found.")
    else:
        for item in items:
            menu_item = MenuItem(item[0], item[1], item[2], item[3])
            print(menu_item)

#Example
if __name__ == '__main__':
    #create_menu_item("Pizza", "Main Course", 15.99)
    list_menu_items()