import pymysql
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

import time
import datetime
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'a'

app.config['MYSQL_HOST'] = 'sql4.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql4422840'
app.config['MYSQL_PASSWORD'] = 'RVhIWY558M'
app.config['MYSQL_DB'] = 'sql4422840'

mysql = MySQL(app)
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers")

    data1 = cursor.fetchall()

    return render_template('index.html', data=data1)


@app.route('/transaction', methods=['GET', 'POST'])
def make():
    msg = 'Please enter details to be added'
    if request.method == 'POST' and 'cid' in request.form and 'cname' in request.form and 'cemail' in request.form and 'cbal' in request.form:
        user = request.form['cname']
        id = request.form['cid']
        email = request.form['cemail']
        bal = request.form['cbal']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name,id FROM customers WHERE id=%s", (id,))
        pid = cursor.fetchall()
        return render_template('make.html', value=pid, value1=user, value2=id, value3=email, value4=bal)


@app.route("/transactions", methods=['GET', 'POST'])
def transact():
    if request.method == 'POST' and 'reciever' in request.form and 'amount' in request.form and 'pname' in request.form and 'pbal' in request.form:
        reciever = request.form['reciever']
        amount = float(request.form['amount'])
        amount1 = float(request.form['amount'])
        sender = request.form['pname']
        scurrbal = float(request.form['pbal'])
        cursor = mysql.connection.cursor()
        sbal = scurrbal - amount
        cursor.execute(
            "SELECT curr_bal FROM customers WHERE name=%s", (reciever,))
        rcurr_bal = cursor.fetchone()
        rcurrbal = float(rcurr_bal[0])
        rbal = rcurrbal + amount1
        print(rcurrbal)
        print(rbal)
        cursor.execute("SELECT * FROM transactions WHERE sname=%s", (sender,))

        tid = cursor.fetchall()
        if scurrbal >= amount:
            cursor.execute(
                "UPDATE customers SET curr_bal=%s where name=%s", (rbal, reciever,))
            cursor.execute(
                "UPDATE customers SET curr_bal=%s where name=%s", (sbal, sender,))
            cursor.execute("INSERT INTO transactions(sname,rname,amount) VALUES ( %s, %s,%s)",
                           (sender, reciever, amount,))
            mysql.connection.commit()
        else:
            return "Insufficient Funds!"
        return redirect(url_for('transhis'))
        # return render_template('transact.html', value=tid)


@app.route('/history')
def transhis():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY time DESC')
    data1 = cursor.fetchall()
    return render_template('tranhis.html', data=data1)


if __name__ == "__main__":
    app.run(debug=True)
