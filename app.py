from flask import Flask, render_template_string, request, redirect, session
from inventory_manager import InventoryManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
manager = InventoryManager()

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    inventory = manager.get_inventory()
    is_admin = session['username'] == 'admin'
    return render_template_string('''
        <h1>Dashboard</h1>
        <h2>Inventory</h2>
        <pre>{{ inventory }}</pre>
        <a href="/orders">View Orders</a>
        <a href="/place_order">Place Order</a>
        {% if is_admin %}
        <a href="/top_selling_items">Top Selling Items</a>
        <a href="/add_item">Add Item</a>
        <a href="/update_item">Update Item</a>
        <a href="/delete_item">Delete Item</a>
        {% endif %}
        <a href="/logout">Logout</a>
    ''', inventory=inventory, is_admin=is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if manager.authenticate(username, password):
            session['username'] = username
            return redirect('/')
        return 'Login failed.'
    return render_template_string('''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/orders')
def orders():
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    if username == 'admin':
        user_orders = manager.orders
    else:
        user_orders = {oid: o for oid, o in manager.orders.items() if o['username'] == username}
    return render_template_string('''
        <h1>Orders</h1>
        <pre>{{ orders }}</pre>
        <a href="/">Back to Dashboard</a>
    ''', orders=user_orders)

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if 'username' not in session:
        return redirect('/login')
    inventory = manager.get_inventory()
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])
        result, msg = manager.place_order(session['username'], item_id, quantity)
        return msg
    # Show order form on GET with item_id dropdown
    return render_template_string('''
        <h1>Place Order</h1>
        <form method="post">
            Item ID:
            <select name="item_id">
                {% for id, item in inventory.items() %}
                    <option value="{{ id }}">{{ id }} - {{ item['name'] }}</option>
                {% endfor %}
            </select><br>
            Quantity: <input name="quantity" type="number"><br>
            <input type="submit" value="Place Order">
        </form>
        <a href="/">Back to Dashboard</a>
    ''', inventory=inventory)

@app.route('/top_selling_items')
def top_selling_items():
    if 'username' not in session:
        return redirect('/login')
    items = manager.top_selling_items()
    return render_template_string('''
        <h1>Top Selling Items</h1>
        <pre>{{ items }}</pre>
        <a href="/">Back to Dashboard</a>
    ''', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        item_id = request.form['item_id']
        name = request.form['name']
        quantity = int(request.form['quantity'])
        result, msg = manager.add_item(item_id, name, quantity)
        return msg
    return render_template_string('''
        <h1>Add Item</h1>
        <form method="post">
            Item ID: <input name="item_id"><br>
            Name: <input name="name"><br>
            Quantity: <input name="quantity" type="number"><br>
            <input type="submit" value="Add Item">
        </form>
        <a href="/">Back to Dashboard</a>
    ''')

@app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    if 'username' not in session:
        return redirect('/login')
    inventory = manager.get_inventory()
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])
        result, msg = manager.update_item(item_id, quantity)
        return msg
    return render_template_string('''
        <h1>Update Item</h1>
        <form method="post">
            Item ID:
            <select name="item_id">
                {% for id, item in inventory.items() %}
                    <option value="{{ id }}">{{ id }} - {{ item['name'] }}</option>
                {% endfor %}
            </select><br>
            Quantity: <input name="quantity" type="number"><br>
            <input type="submit" value="Update Item">
        </form>
        <a href="/">Back to Dashboard</a>
    ''', inventory=inventory)

@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    if 'username' not in session:
        return redirect('/login')
    inventory = manager.get_inventory()
    if request.method == 'POST':
        item_id = request.form['item_id']
        result, msg = manager.delete_item(item_id)
        return msg
    return render_template_string('''
        <h1>Delete Item</h1>
        <form method="post">
            Item ID:
            <select name="item_id">
                {% for id, item in inventory.items() %}
                    <option value="{{ id }}">{{ id }} - {{ item['name'] }}</option>
                {% endfor %}
            </select><br>
            <input type="submit" value="Delete Item">
        </form>
        <a href="/">Back to Dashboard</a>
    ''', inventory=inventory)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
