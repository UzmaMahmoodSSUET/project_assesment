from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "peloris_100",
    "database": "managment_system"
}

users = []
products = []

# Helper function to execute a query and fetch data from the database
def execute_query(query, params=None, fetch_one=False):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params)
        connection.commit()

        if fetch_one:
            data = cursor.fetchone()
        else:
            data = cursor.fetchall()

        return data
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Endpoint for user registration
@app.route('/registeruser', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({"error": "Incomplete user data"}), 400

        # Check if the email is already registered
        email_check_query = "SELECT id FROM users WHERE email = %s"
        email_check_result = execute_query(email_check_query, (email,), fetch_one=True)

        if email_check_result:
            return jsonify({"error": "Email already registered"}), 400

        # Insert user data into the 'users' table
        insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        execute_query(insert_query, (username, email, password))
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Registration failed"}), 500

# Endpoint to get all products
@app.route('/getallproducts', methods=['GET'])
def get_all_products():
    try:
        query = "SELECT * FROM products"
        products_data = execute_query(query)
        return jsonify(products_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve products"}), 500

# Endpoint for placing an order
@app.route('/order', methods=['POST'])
def place_order():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not user_id or not product_id or not quantity:
            return jsonify({"error": "Incomplete order data"}), 400

        # Check if the user and product exist
        user_check_query = "SELECT id FROM users WHERE id = %s"
        product_check_query = "SELECT id, price FROM products WHERE id = %s"
        
        user_check_result = execute_query(user_check_query, (user_id,), fetch_one=True)
        product_check_result = execute_query(product_check_query, (product_id,), fetch_one=True)

        if not user_check_result or not product_check_result:
            return jsonify({"error": "User or product not found"}), 404

        total_price = product_check_result['price'] * quantity

        # Insert order data into the 'orders' table
        insert_query = "INSERT INTO orders (user_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)"
        execute_query(insert_query, (user_id, product_id, quantity, total_price))
        return jsonify({"message": "Order placed successfully"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Order placement failed"}), 500

# Endpoint to retrieve all orders
@app.route('/allorders', methods=['GET'])
def get_all_orders():
    try:
        query = "SELECT * FROM orders"
        orders_data = execute_query(query)
        return jsonify(orders_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve orders"}), 500

# Endpoint to add a product
@app.route('/addproduct', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')

        if not name or not price:
            return jsonify({"error": "Incomplete product data"}), 400

        # Insert product data into the 'products' table
        insert_query = "INSERT INTO products (name, price) VALUES (%s, %s)"
        execute_query(insert_query, (name, price))
        return jsonify({"message": "Product added successfully"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Product addition failed"}), 500

# Endpoint to update a product
@app.route('/updateproduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')

        if not name or not price:
            return jsonify({"error": "Incomplete product data"}), 400

        # Check if the product exists
        product_check_query = "SELECT id FROM products WHERE id = %s"
        product_check_result = execute_query(product_check_query, (product_id,), fetch_one=True)

        if not product_check_result:
            return jsonify({"error": "Product not found"}), 404

        # Update product data in the 'products' table
        update_query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
        execute_query(update_query, (name, price, product_id))
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Product update failed"}), 500

# Endpoint to delete a product
@app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        # Check if the product exists
        product_check_query = "SELECT id FROM products WHERE id = %s"
        product_check_result = execute_query(product_check_query, (product_id,), fetch_one=True)

        if not product_check_result:
            return jsonify({"error": "Product not found"}), 404

        # Delete the product from the 'products' table
        delete_query = "DELETE FROM products WHERE id = %s"
        execute_query(delete_query, (product_id,))
        return jsonify({"message": "Product deleted successfully"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Product deletion failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)