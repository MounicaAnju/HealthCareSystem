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
            password=data['password']
            conn = sqlite3.connect('database.db')
            print ("Opened database successfully")
            conn.execute('drop table users')
            conn.execute('CREATE TABLE IF NOT EXISTS USERS(fname TEXT, lname TEXT, age TEXT, address TEXT, gender TEXT, email TEXT,phonenumber TEXT,password TEXT)')
            print ("Table created successfully")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO USERS (fname, lname, age, address, gender, email,phonenumber,password) VALUES(?,?,?,?,?,?,?,?)",(fname, lname, age, address, gender, email,phonenumber,password))
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
        
@app.route("/uservalidation", methods=['POST'])
def uservalidation():
    email = request.json['email']
    password = request.json['password']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    user = cursor.fetchone()
    if user:
        # User is found, return JSON response indicating success
        return jsonify(valid=True)
    else:
        # User is not found, return JSON response indicating failure
        return jsonify(valid=False)

            
@app.route("/contactusform", methods=['POST'])
def contactusform():
    if request.method == 'POST':
        form = request.json
        name = form['name']
        email = form['email']
        message = form['message']
        try:
            conn = sqlite3.connect('database.db')
            print("Opened database successfully")
            conn.execute('drop table if exists contactus')
            conn.execute('CREATE TABLE IF NOT EXISTS CONTACTUS(name TEXT, email TEXT,message TEXT)')
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO CONTACTUS (name, email, message) VALUES (?, ?, ?)", (name, email, message))
                con.commit()
                msg = "Record added successfully"
        except:
            con.rollback()
            msg = "Data Insertion Failed"

        finally:
            con.close()
            return jsonify({'message': msg})









