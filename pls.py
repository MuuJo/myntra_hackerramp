import mysql.connector
from flask import Flask, render_template

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="exptracker"
)

app = Flask(__name__, template_folder="D:/OneDrive/Mukta_OneDrive/Mukta_exploration/Myntra_2024/Database/templates")

# Create a database cursor
mycursor = mydb.cursor()

@app.route('/')
def home_page():
    # Simple route to display the HTML page
    return render_template("shared_cart.html")

@app.route('/place_order')
def place_order():
    # Render a new template for the place order page
    return render_template("paymentpage.html")

@app.route('/5050.html')
def fofo():
    # Query data from the 'fofo' table
    mycursor.execute("SELECT * FROM fofo")
    data = mycursor.fetchall()  # Fetch all rows from the result

    # Pass the data to the template
    return render_template("5050.html")

@app.route('/onedone.html')
def oad():
    # Query data from the 'fofo' table
    mycursor.execute("SELECT * FROM oad")
    data = mycursor.fetchall()  # Fetch all rows from the result

    # Pass the data to the template
    return render_template("onedone.html")

@app.route('/godutch.html')
def gd():
    # Query data from the 'fofo' table
    mycursor.execute("SELECT * FROM gd")
    data = mycursor.fetchall()  # Fetch all rows from the result

    # Pass the data to the template
    return render_template("godutch.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002, use_reloader=False)
