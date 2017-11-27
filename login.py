from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/login')
def login():
    return render_template('login.html')

# authenticates logins
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():

    # gets values from login form fields
    username = request.form['username']
    password = request.form['password']

    # initializes & conducts queries to validate login credentials
    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE username = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()

    # if credentials are found in the database, user is logged in
    if(data):
        session['logged_in'] = True
        session['username'] = username
        # redirect to homepage
        return redirect(url_for('main', username=session['username']))
    else: # credentials are not found
        error = "Invalid login or username/password"
        return render_template('login.html', error=error)
