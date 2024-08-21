import mysql.connector
from flask import Flask, render_template, request,session
from flask_session import Session
import json
import math

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="myntra"
)

app = Flask(__name__, template_folder="D:/OneDrive/Mukta_OneDrive/Mukta_exploration/Myntra_2024/Database/templates")

# Configure Flask session
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the filesystem
Session(app)  # Initialize the session extension

# Create a database cursor
database = mydb
mycursor = database.cursor()

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route("/form_login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]

    mycursor.execute("SELECT password FROM users WHERE username=%s", (user,))
    result = mycursor.fetchone()

    if result:
        stored_pass = result[0]
        if stored_pass != pwd:
            return render_template("login.html", info="Invalid Password")
        else:
            session['username']=user
            return render_template("home8.html")
    else:
        return render_template("login.html", info="User not found")

@app.route('/home8.html')
def home_page():
    return render_template("home8.html")

@app.route('/aesthetic')
def aesthetic_page():
    return render_template("aesthetic8.html")

@app.route('/lead6.html')
def lead_page():
    return render_template("lead6.html")

@app.route('/profile2.html')
def profile_page():
    
    # Query to get all aesthetic names from the build_aesthetics table
    mycursor.execute("SELECT name FROM build_aesthetics")
    aesthetic_names = mycursor.fetchall()

    # Pass the aesthetic names to the profile1.html template
    return render_template("profile2.html", aesthetic_names=aesthetic_names)

@app.route('/index1.html')
def build_aesthetic():
    return render_template("index1.html")

@app.route('/product-shirts.html')
def product_shirts():
    return render_template('product-shirts.html')

@app.route('/products-pants.html')
def products_pants():
    return render_template('products-pants.html')

@app.route('/shirt-3-pant.html')
def shirt_2_pant():
    return render_template('shirt-3-pant.html')

@app.route('/white_shirt_chosen.html')
def white_shirt_chosen():
    return render_template('white_shirt_chosen.html')

@app.route('/add_name', methods=["POST"])
def add_name():
    aesthetic_name = request.form["aesthetic_name"]
    
    insert_query = "INSERT INTO build_aesthetics (name) VALUES (%s)"
    
    try:
        mycursor.execute(insert_query, (aesthetic_name,))
        database.commit()
        return render_template("index1.html", message=f"Name '{aesthetic_name}' added successfully.")
    except mysql.connector.Error as err:
        return render_template("index1.html", error=f"Error: {err}")

@app.route('/save_items', methods=['POST'])
def save_items():
    aesthetic_name = request.form.get('aesthetic_name')
    items = request.form.get('items')
    
    if not aesthetic_name or not items:
        return 'Error: Missing data', 400
    
    items = json.loads(items)

    insert_query = "INSERT INTO selected_items (aesthetic_name, item_name) VALUES (%s, %s)"
    try:
        for item in items:
            mycursor.execute(insert_query, (aesthetic_name, item))
        database.commit()
        return 'Success', 200
    except mysql.connector.Error as err:
        return f"Error: {err}", 500


@app.route('/shared_cart.html')
def shared_cart():
    username = session.get('username')
    if not username:
        return "User not logged in", 403

    try:
        

        # Query to get distinct items from shared_cart_items table
        query_items = """
        SELECT s.article_id, s.name, s.description, s.price, s.image, MIN(u.username) as username
        FROM shared_cart_items s
        JOIN shared_cart_users sc ON s.shared_cart_id = sc.shared_cart_id
        JOIN users u ON sc.user_id = u.user_id
        WHERE sc.shared_cart_id = (
            SELECT shared_cart_id
            FROM shared_cart_users
            WHERE user_id = (
                SELECT user_id
                FROM users
                WHERE username = %s
            )
        )
        GROUP BY s.article_id, s.name, s.description, s.price, s.image
        """

        mycursor.execute(query_items, (username,))
        items = mycursor.fetchall()

        # Query to get all usernames for the current cart
        query_users = """
        SELECT DISTINCT u.username
        FROM shared_cart_users sc
        JOIN users u ON sc.user_id = u.user_id
        WHERE sc.shared_cart_id = (
            SELECT shared_cart_id
            FROM shared_cart_users
            WHERE user_id = (
                SELECT user_id
                FROM users
                WHERE username = %s
            )
        )
        """

        mycursor.execute(query_users, (username,))
        users = mycursor.fetchall()

        # Process the results for users
        user_list = [user[0] for user in users]  # Extract usernames from the result tuples

        # Pass the data to the template
        return render_template("shared_cart.html", items=items, users=user_list)

    except mysql.connector.Error as err:
        return f"Database error: {err}", 500


@app.route('/place_order')
def place_order():
    # Render a new template for the place order page
    return render_template("paymentpage.html")

@app.route('/5050.html')
def fofo():

    username = session.get('username')
    if not username:
        return "User not logged in", 403

    # Query to get all items from the 'fofo' table
    query_all = """
    SELECT f.article_id, f.name, f.description, f.price, f.image
    FROM fofo f
    """
    mycursor.execute(query_all)
    all_items = mycursor.fetchall()  # Fetch all rows from the result

    # Query to get the sum of all item prices
    query_sum = """
    SELECT SUM(price) FROM fofo
    """
    mycursor.execute(query_sum)
    total_sum_result = mycursor.fetchone()
    total_sum = total_sum_result[0] if total_sum_result[0] is not None else 0

    # Query to get the total number of distinct users
    query_user_count = """
    SELECT COUNT(DISTINCT username) FROM users
    """
    mycursor.execute(query_user_count)
    user_count_result = mycursor.fetchone()
    user_count = user_count_result[0] if user_count_result[0] is not None else 1  # Avoid division by zero

    # Calculate amount payable (sum of all item prices divided by number of distinct users)
    amount_payable = total_sum / user_count
    
    # Round up the amount payable to the nearest whole number
    amount_payable_rounded = math.ceil(amount_payable)

    # Pass the data and rounded amount payable to the template
    return render_template("5050.html", all_items=all_items, amount_payable=amount_payable_rounded)


@app.route('/onedone.html')
def oad():
    username = session.get('username')
    if not username:
        return "User not logged in", 403

    # Query to get all items from the 'oad' table
    query_all = """
    SELECT o.article_id, o.name, o.description, o.price, o.image
    FROM oad o
    """
    mycursor.execute(query_all)
    all_items = mycursor.fetchall()  # Fetch all rows from the result

    # Query to get the sum of all item prices in the 'oad' table
    query_sum = """
    SELECT SUM(price) FROM oad
    """
    mycursor.execute(query_sum)
    total_sum_result = mycursor.fetchone()
    total_sum = total_sum_result[0] if total_sum_result[0] is not None else 0

    # Calculate amount payable (sum of all item prices in 'oad')
    amount_payable = total_sum
    
    # Round up the amount payable to the nearest whole number
    amount_payable_rounded = math.ceil(amount_payable)

    # Pass the data and rounded amount payable to the template
    return render_template("onedone.html", all_items=all_items, amount_payable=amount_payable_rounded)
@app.route('/godutch.html')
def gd():
    username = session.get('username')
    if not username:
        return "User not logged in", 403

    # Query to get all items from the 'gd' table
    query_all = """
    SELECT g.article_id, g.name, g.description, g.price, g.image
    FROM gd g
    """
    mycursor.execute(query_all)
    all_items = mycursor.fetchall()  # Fetch all rows from the result

    # Query to get items specific to the logged-in user
    query_user = """
    SELECT g.price
    FROM gd g
    JOIN users u ON g.user_id = u.user_id
    WHERE u.username = %s
    """
    mycursor.execute(query_user, (username,))
    user_items = mycursor.fetchall()  # Fetch all rows for the logged-in user

    # Calculate total amount payable for the logged-in user
    total_amount = sum(row[0] for row in user_items)  # Sum of all prices for the user
    amount_payable = total_amount

    # Pass the data and amount payable to the template
    return render_template("godutch.html", all_items=all_items, amount_payable=amount_payable)



if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)
