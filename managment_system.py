from flask import Flask, request, jsonify
from flask_mysqldb import MySQL  
app = Flask(__name__)
mysql = MySQL(app)
app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = "peloris_100"
app.config ['MYSQL_DB'] = 'management_system'

# Create an empty list to store registered users
registered_users = []

@app.route('/registeruser', methods=['POST'])
def register_user():
    data = request.get_json()  # Parse the JSON data from the request
    # Check if the required fields are in the request data
    if 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create a new user object and add it to the list
    username = data['username']
    email = data['email']
    
    cur =mysql.connection.cursor()
    cur.execute("INSERT INTO users(name,email) VALUES(%s,%s)",(username,email))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User registered successfully'}),201

# Sample data for orders
orders = []

@app.route('/order', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'GET':
        # Return a list of orders
        return jsonify(orders)
    elif request.method == 'POST':
        # Create a new order
        data = request.json
        if 'customer' in data and 'product' in data and 'quantity' in data:
            new_order = {
                'customer': data['user_id'],
                'product': data['product_id'],
                'quantity': data['quantity']
            }
            orders.append(new_order)
            return jsonify({'message': 'Order created successfully'}), 201
        else:
            return jsonify({'error': 'Incomplete order data'}), 400

# Sample data for orders (you can replace this with your actual data)
orders = [
   {
        "customer": "uzma",
        "product": "product1",
        "quantity": "3"
    },
    {
        "customer": "asma",
        "product": "product2",
        "quantity": "3"
    },
    {
        "customer": "mehwish",
        "product": "product3",
        "quantity": "4"
    },
    {'customer': 'fareha',
        'product_name': 'product2',
        'quantity': "3",
    },
]

# Endpoint to get all orders
@app.route('/allorders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders})





# Sample product data (you would typically fetch this from a database)
products = [
    {"id": 1, "name": "Product 1", "price": 10.99},
    {"id": 2, "name": "Product 2", "price": 19.99},
    {"id": 3, "name": "Product 3", "price": 5.99},
]

@app.route('/getallproducts', methods=['GET'])
def get_all_products():
    return jsonify(products)


# Sample data to store products

# Endpoint to add a product
@app.route('/addproduct', methods=['POST'])
def add_product():
  
        # Parse JSON data from the request
        data = request.get_json()

        # Validate the request data
        if 'name' not in data or 'price' not in data:
            return jsonify({"error": "Name and price are required"}), 400

        # Create a new product
        product = {
             "id":data["id"],
            'name': data['name'],
            'price': data['price']
        }
        products.append(product)

        # Add the product to the list
        products.append(product)

        return jsonify({"message": "Product added successfully"}), 201

#update and delete a product



# Endpoint to update a product
@app.route('/updateproduct/<int:product_id>', methods=['PUT'])
   
def update_product(product_id):
    id=product_id
    if id not in products:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if "name" in data:
        products[id]["name"] = data["name"]
    if "price" in data:
        products[id]["price"] = data["price"]

    return jsonify(products[id])

# Endpoint to delete a product
@app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if product_id not in products:
        return jsonify({"error": "Product not found"}), 404

    del products[product_id]
    return jsonify({"message": "Product deleted"})

if __name__ == '__main__':
    app.run(debug=True)
