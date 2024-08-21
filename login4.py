import mysql.connector
from flask import Flask, render_template, request
import json

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="myntra"
)

app = Flask(__name__, template_folder="D:/OneDrive/Mukta_OneDrive/Mukta_exploration/Myntra_2024/Database/templates")

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
    # Simple route to display the HTML page
    return render_template("shared_cart.html")

@app.route('/place_order')
def place_order():
    # Render a new template for the place order page
    return render_template("paymentpage.html")

@app.route('/5050.html')
def fofo():
     # Query data from the 'fofo' table and join with 'users' table to get username
    query = """
    SELECT f.article_id, f.name, f.description, f.price, f.image, u.username
    FROM fofo f
    JOIN users u ON f.user_id = u.user_id
    """
    mycursor.execute(query)
    data = mycursor.fetchall()  # Fetch all rows from the result

    # Pass the data to the template
    return render_template("5050.html", data=data)
@app.route('/onedone.html')
def oad():
    # Query data from the 'fofo' table
    mycursor.execute("SELECT * FROM oad")
    data = mycursor.fetchall()  # Fetch all rows from the result

    # Pass the data to the template
    return render_template("onedone.html",data=data)

@app.route('/godutch.html')
def gd():
    # Query data from the 'fofo' table
    mycursor.execute("SELECT * FROM gd")
    data = mycursor.fetchall()  # Fetch all rows from the result

    # Pass the data to the template
    return render_template("godutch.html",data=data)


if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)
