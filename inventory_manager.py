import json
import threading
import time
from werkzeug.security import generate_password_hash, check_password_hash

class InventoryManager:
    def __init__(self):
        self.inventory = self.load_json('inventory.json')
        self.users = self.load_json('users.json')
        self.orders = self.load_json('orders.json')
        self.logs = self.load_json('logs.json')
        self.lock = threading.Lock()
        self.auto_save_thread = threading.Thread(target=self.auto_save, daemon=True)
        self.auto_save_thread.start()

    def load_json(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_json(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def auto_save(self):
        while True:
            # BUG: Concurrency issue, not using lock for saving
            self.save_json('inventory.json', self.inventory)
            self.save_json('users.json', self.users)
            self.save_json('orders.json', self.orders)
            self.save_json('logs.json', self.logs)
            time.sleep(10)

    # User authentication
    def register_user(self, username, password):
        if username in self.users:
            return False, 'User already exists.'
        # Store hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        self.users[username] = {'password': hashed_password}
        return True, 'User registered.'

    def authenticate(self, username, password):
        user = self.users.get(username)
        if not user:
            return False
        stored_password = user['password']
        # Try to authenticate as hash
        try:
            if check_password_hash(stored_password, password):
                return True
        except Exception:
            pass
        # Fallback: check plain text
        if stored_password == password:
            # Migrate to hash
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            self.users[username]['password'] = hashed_password
            return True
        return False

    # Inventory CRUD
    def add_item(self, item_id, name, quantity):
        if item_id in self.inventory:
            return False, 'Item already exists.'
        if quantity < 0:
            return False, 'Quantity cannot be negative.'
        self.inventory[item_id] = {'name': name, 'quantity': quantity}
        return True, 'Item added.'

    def update_item(self, item_id, quantity):
        if item_id not in self.inventory:
            return False, 'Item not found.'
        if quantity < 0:
            return False, 'Quantity cannot be negative.'
        self.inventory[item_id]['quantity'] = quantity
        return True, 'Item updated.'

    def delete_item(self, item_id):
        if item_id in self.inventory:
            del self.inventory[item_id]
            return True, 'Item deleted.'
        return False, 'Item not found.'

    def get_inventory(self):
        return self.inventory

    # Order placement
    def place_order(self, username, item_id, quantity):
        if username not in self.users:
            return False, 'User not found.'
        if item_id not in self.inventory:
            return False, 'Item not found.'
        if quantity < 0:
            return False, 'Invalid quantity.'
        # Check if enough stock is available
        if self.inventory[item_id]['quantity'] < quantity:
            return False, 'Not enough stock.'
        # Reduce inventory quantity
        self.inventory[item_id]['quantity'] -= quantity
        order_id = str(len(self.orders) + 1)
        self.orders[order_id] = {
            'username': username,
            'item_id': item_id,
            'quantity': quantity,
            'timestamp': time.time()
        }
        self.logs[str(time.time())] = f"Order placed by {username} for {quantity} of {item_id}"
        return True, 'Order placed.'

    # Analytics
    def top_selling_items(self):
        sales = {}
        for order in self.orders.values():
            item_id = order['item_id']
            qty = order['quantity']
            # Sum quantities for each item
            sales[item_id] = sales.get(item_id, 0) + qty
        sorted_items = sorted(sales.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:3]

    # Logging
    def log_event(self, event):
        self.logs[str(time.time())] = event

    # Error handling missing for edge cases (e.g., negative inventory)
