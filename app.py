from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import sqlite3
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/aboutus")
def aboutus():
    return render_template("about-us.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/bookappointment")
def bookappointment():
    return render_template("bookappointment.html")

@app.route("/contactus")
def contactus():
    return render_template("contact-us.html")

@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword.html")

@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/createaccount")
def createaccount():
    return render_template("createaccount.html")

@app.route("/db")
def db():
    conn = sqlite3.connect('database.db')
    print ("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS USERS(fname TEXT, lname TEXT)')
    print ("Table created successfully")
    conn.close()
    return "Table created successfully"

@app.route("/addrow", methods=['POST','GET'])
def addrow():
    print("hiiiiiiiiii")
    if request.method == 'POST':
        try:
            data = request.get_json()
            fname = data['firstName']
            lname = data['lastName']
            age = data['age']
            address = data['address']
            gender = data['gender']
            email = data['email']
            phonenumber = data['phoneno']
            conn = sqlite3.connect('database.db')
            print ("Opened database successfully")
            conn.execute('CREATE TABLE IF NOT EXISTS USERS(fname TEXT, lname TEXT, age TEXT, address TEXT, gender TEXT, email TEXT,phonenumber TEXT)')
            print ("Table created successfully")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO USERS (fname, lname, age, address, gender, email,phonenumber) VALUES(?,?,?,?,?,?,?)",(fname, lname, age, address, gender, email,phonenumber))
                # cur.execute("INSERT INTO USERS (fname, lname) VALUES(?,?)",(fname, lname ))
                print("hello db")
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            print("hello error")
            msg = "error in insert operation"
        
        finally:
            
            con.close()
            return jsonify({'message': msg})
            
        



