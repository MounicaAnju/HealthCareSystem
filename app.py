from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
import json
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
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT doctor FROM appointments")
    rows = cursor.fetchall()
    professionals = ["Pediatrician", "Cardiologist", "Dentist", "Chiropractor", "Ophthalmologist", "Dermatologist", "Gastroenterologist"]
    count_by_professional = {professional: 0 for professional in professionals}
    for row in rows:
        doctor = row[0]
        specialty = doctor.split(" - ")[1]
        if specialty in count_by_professional:
            count_by_professional[specialty] += 1
    professionalscounts = [count_by_professional[professional] for professional in professionals]

    cursor.execute("SELECT strftime('%m', datetime) as month FROM appointments")
    results = cursor.fetchall()
    month_counts = {}
    for result in results:
        month_num = int(result[0])
        month_name = datetime(2000, month_num, 1).strftime('%b')
        if month_name in month_counts:
            month_counts[month_name] += 1
        else:
            month_counts[month_name] = 1
            
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    counts = []
    for label in labels:
        if label in month_counts:
            counts.append(month_counts[label])
        else:
            counts.append(0)

    return render_template("analytics.html", labels=json.dumps(labels), counts=json.dumps(counts), professionals=json.dumps(professionals), professionalscounts=json.dumps(professionalscounts))

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
            # conn.execute('drop table users')
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
        
@app.route("/addappointment", methods=['POST','GET'])
def addappointment():
    if request.method == 'POST':
        try:
            data = request.get_json()
            fname = data['firstName']
            lname = data['lastName']
            age = data['age']
            address = data['address']
            gender = data['gender']
            email = data['email']
            phoneNumber = data['phoneNumber']
            doctor = data['doctor']
            datetime = data['datetime']
            msg = data['msg']
            conn = sqlite3.connect('database.db')
            print ("Opened database successfully")
            # conn.execute('drop table users')
            conn.execute('CREATE TABLE IF NOT EXISTS APPOINTMENTS(fname TEXT, lname TEXT, age TEXT, address TEXT, gender TEXT, email TEXT,phonenumber TEXT,doctor TEXT, datetime timestamp, msg TEXT)')
            print ("Table created successfully")

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO APPOINTMENTS (fname, lname, age, address, gender, email, phonenumber,doctor,datetime,msg ) VALUES(?,?,?,?,?,?,?,?,?,?)",(fname, lname, age, address, gender, email, phoneNumber,doctor, datetime, msg))
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
        

@app.route('/validate', methods=['POST'])
def validate():
    email = request.json['email']
    password = request.json['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    # print(result[7])

    conn.close()

    if result:
        if result[7] == password:
            # name=result[0]
            print("hiiiiii user")
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'})
    else:
        # User does not exist
        return jsonify({'success': False})


    # print("hiii")
    # email = request.json['email']
    # password = request.json['password']
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    # user = cursor.fetchone()
    # if user:
    #     # User is found, return JSON response indicating success
    #     return jsonify(valid=True)
    # else:
    #     # User is not found, return JSON response indicating failure
    #     return jsonify(valid=False)