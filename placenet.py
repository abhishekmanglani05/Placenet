# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
  
  
# app = Flask(__name__)
  
  
# app.secret_key = 'xyzsdfg'
  
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'user-system'
  
# mysql = MySQL(app)
  
# @app.route('/')
# @app.route('/login', methods =['GET', 'POST'])
# def login():
#     mesage = ''
#     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
#         email = request.form['email']
#         password = request.form['password']
#         cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
#         user = cursor.fetchone()
#         if user:
#             session['loggedin'] = True
#             session['userid'] = user['userid']
#             session['name'] = user['name']
#             session['email'] = user['email']
#             mesage = 'Logged in successfully !'
#             return render_template('user.html', mesage = mesage)
#         else:
#             mesage = 'Please enter correct email / password !'
#     return render_template('login.html', mesage = mesage)
  
# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('userid', None)
#     session.pop('email', None)
#     return redirect(url_for('login'))
  
# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     mesage = ''
#     if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
#         userName = request.form['name']
#         password = request.form['password']
#         email = request.form['email']
#         cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
#         account = cursor.fetchone()
#         if account:
#             mesage = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             mesage = 'Invalid email address !'
#         elif not userName or not password or not email:
#             mesage = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO user VALUES (% s, % s, % s)', (userName, email, password))
#             mysql.connect.commit()
#             mesage = 'You have successfully registered !'
#     elif request.method == 'POST':
#         mesage = 'Please fill out the form !'
#     return render_template('register.html', mesage = mesage)
    
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pickle
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import warnings
import numpy as np
import random
from random import choice, sample

model = pickle.load(open("C:\\Users\\Dell\\complete web development\\placenet\\placement_prediction_model", "rb"))
  
  
app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        # cursor.execute(f'SELECT * FROM user WHERE email = "{email}" AND password = "{password}"')
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            # session['userid'] = user['userid']
            session['name'] = user['name']
            email_a = user['email']
            branch= user['Branch']
            roll_no= user['Roll_no']
            score_10= user['10th_Score']
            score_12= user['12th_Score']
            cgpa= user['CGPA']
            attendence= user['Attendance']
            mesage = 'Logged in successfully !'
            return render_template('user.html', d=email_a, b=branch, c=roll_no, e=score_10, f=score_12, g=attendence, h=cgpa)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    # session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']

        try:
            conn = mysql.connect

            if conn:
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        # cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
                account = cursor.fetchone()
                if account:
                    mesage = 'Account already exists !'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    mesage = 'Invalid email address !'
                elif not userName or not password or not email:
                    mesage = 'Please fill out the form !'
                else:
                    cursor.execute('INSERT INTO user (name, email, password) VALUES (% s, % s, % s)', (userName, email, password ))
                    # cursor.execute(f'INSERT INTO user (name, email, password) VALUES ({userName}, {email}, {password})')
                    conn.commit()
                    cursor.close()
                    mesage = 'You have successfully registered !'

            else:
                return "Connection not established."
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
                
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)



@app.route('/edit', methods =['GET', 'POST'])
def edit():
    # message=""
    email = request.form['email']
    data1 = request.form['branch']
    data2 = request.form['roll no']
    data3 = request.form['10th Percentage']
    data4 = request.form['12th Percentage']
    data5 = request.form['CGPA']
    data6 = request.form['Attendence']
    try:
        conn = mysql.connect
        if conn:
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        # cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE user set Branch= % s, Roll_no= %s, 10th_Score= %s, 12th_Score= %s, CGPA= %s, Attendance= %s WHERE email= % s ', (data1, data2, data3, data4, data5, data6, email) )
                conn.commit()
                cursor.close()
                return render_template("success.html")
                # message="success"
        else:
            return "connection not extablished"
    
    except Exception as e:
            return f"An error occurred: {str(e)}"
    


@app.route('/edit01')
def edit01():
    return render_template('edit01.html')

@app.route('/login01')
def login01():
    return render_template('login01.html')


#get data 
sql="SELECT * FROM user WHERE Branch=AIML;"
@app.route('/login01a', methods =['GET', 'POST'])
def login01a():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usersss WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            # session['userid'] = user['userid']
            session['name'] = user['name']
            email_a = user['email']
            # branch= user['Branch']
            # roll_no= user['Roll_no']
            # score_10= user['10th_Score']
            # score_12= user['12th_Score']
            # cgpa= user['CGPA']
            # attendence= user['Attendance']
            # mesage = 'Logged in successfully !'

            #get data
            # cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute("SELECT name, email FROM user WHERE Branch='AIML';")
            # myresult=cursor.fetchall()
            return render_template('user01.html', d=email_a)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login01.html', mesage = mesage)


@app.route('/register01', methods =['GET', 'POST'])
def register01():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']

        try:
            conn = mysql.connect

            if conn:
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        # cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM usersss WHERE email = % s', (email, ))
                account = cursor.fetchone()
                if account:
                    mesage = 'Account already exists !'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    mesage = 'Invalid email address !'
                elif not userName or not password or not email:
                    mesage = 'Please fill out the form !'
                else:
                    cursor.execute('INSERT INTO usersss (name, email, password) VALUES (% s, % s, % s)', (userName, email, password ))
                    conn.commit()
                    cursor.close()
                    mesage = 'You have successfully registered !'

            else:
                return "Connection not established."
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
                
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register01.html', mesage = mesage)


@app.route('/pred')
def pred():
    return render_template('prediction_page.html')

@app.route('/prediction_page', methods =['GET', 'POST'])
def prediction():
    message=""
    data0 = request.form['communication_skills']
    data1 = request.form['core_branch']
    data2 = request.form['programming_language']
    data3 = request.form['technical_skills']
    data4 = request.form['certification_course']
    data5 = request.form['backlog']
    data6 = request.form['10th Percentage']
    data7 = request.form['12th Percentage']
    data8 = request.form['Attendence']
    data9 = request.form['Company Name']



    
    
    


    # input_data = {
    #     'Communication Skills': [data0],
    #     'Certification Course': [data4],
    #     'Backlog': [data5],
    #     '10th Score (%)': [data6],
    #     '12th Score (%)': [data7],
    #     'Attendance (%)': [data8],
    #     'Core Branch': [data1],
    #     'Programming Language': [data2],
    #     'Other Technical Skills': [data3],
    #     'Company': [data9]
    # }

    df = pd.read_csv('C:\\Users\\Dell\\complete web development\\placenet\\student_dataset.csv')

    X = df.drop('Eligibility', axis=1)  # Features
    y = df['Eligibility']  # Target variable

# Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_encoded = pd.get_dummies(X, columns=['Core Branch', 'Programming Language', 'Other Technical Skills', 'Company'])

# Split the encoded dataset into training and testing sets (80% train, 20% test)
    X_train_encoded, X_test_encoded, y_train_encoded, y_test_encoded = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# # Create an XGBoost classifier
#     xgb_classifier = xgb.XGBClassifier(random_state=42)

# # Train the classifier on the training data
#     xgb_classifier.fit(X_train_encoded, y_train_encoded)

    data = [[data0,data4,data5,data6,data7,data8,data1,data2,data3,data9]]

    
    input_data = pd.DataFrame(data, columns= ['Communication Skills',
        'Certification Course',
        'Backlog',
        '10th Score (%)',
        '12th Score (%)',
        'Attendance (%)',
        'Core Branch',
        'Programming Language',
        'Other Technical Skills',
        'Company'], dtype = ('category'), index = ['input']
    )



    input_df = pd.DataFrame(input_data)

    input_df_encoded = pd.get_dummies(input_df, columns=['Core Branch', 'Programming Language', 'Other Technical Skills', 'Company'])

    missing_features = list(set(X_train_encoded.columns) - set(input_df_encoded.columns))
    for feature in missing_features:
        input_df_encoded[feature] = 0

    # Ensure that only the relevant columns are considered
    input_df_encoded = input_df_encoded[X_train_encoded.columns]

    message = model.predict(input_df_encoded)[0]

    return render_template('after.html', a=message)


@app.route('/output02')
def output02():
    return render_template('output02.html')

@app.route('/output01')
def output01():
    return render_template('output01.html')


@app.route('/search01', methods =['POST'])
def search01():
    search= request.form['search01']

    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT name, email FROM user WHERE Branch= %s",[search])
    myresult=cursor.fetchall()

    return render_template('search01.html', a = myresult)
    # cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute("SELECT name, email FROM user WHERE Branch='%s';")
    # myresult=cursor.fetchall()

    
if __name__ == "__main__":
    app.run(debug=True)