import mysql.connector
from flask import Flask, render_template, request

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

    # Check if user exists
    mycursor.execute("SELECT password FROM users WHERE username=%s", (user,))
    result = mycursor.fetchone()

    if result:
        stored_pass = result[0]
        if stored_pass != pwd:
            # Debugging statement
            print(f"Invalid password for user: {user}")
            return render_template("login.html", info="Invalid Password")
        else:
            # Debugging statement
            print(f"User {user} logged in successfully.")
            return render_template("home8.html")
    else:
        # Debugging statement
        print(f"User not found: {user}")
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

@app.route('/profile.html')
def profile_page():
    return render_template("profile1.html")

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

@app.route('/add_name', methods=["POST"])  # Updated route
def add_name():
    aesthetic_name = request.form["aesthetic_name"]
    
    # SQL query to insert a new record into the build_aesthetics table
    insert_query = "INSERT INTO build_aesthetics (name) VALUES (%s)"
    
    try:
        # Execute the SQL command
        mycursor.execute(insert_query, (aesthetic_name,))
        database.commit()
        
        # Debugging statement
        print(f"Name '{aesthetic_name}' added successfully to build_aesthetics table.")
        
        # Return a success message or redirect to another page
        return render_template("index1.html", message=f"Name '{aesthetic_name}' added successfully.")
    except mysql.connector.Error as err:
        # Debugging statement
        print(f"Error: {err}")
        
        # Return an error message
        return render_template("index1.html", error=f"Error: {err}")

@app.route('/add_item', methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    item_url = request.form["item_url"]
    
    # SQL query to insert a new record into the selected_items table
    insert_query = "INSERT INTO selected_items (item_name, item_url) VALUES (%s, %s)"
    
    try:
        # Execute the SQL command
        mycursor.execute(insert_query, (item_name, item_url))
        database.commit()
        
        # Debugging statement
        print(f"Item '{item_name}' with URL '{item_url}' added successfully to selected_items table.")
        
        # Return a success message or redirect to another page
        return render_template("index1.html", message=f"Item '{item_name}' added successfully.")
    except mysql.connector.Error as err:
        # Debugging statement
        print(f"Error: {err}")
        
        # Return an error message
        return render_template("index1.html", error=f"Error: {err}")

if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)
