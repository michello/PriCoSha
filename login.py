from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/login')
def login():
    return render_template('login.html')

# authenticates logins
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    # username = ml4963
    # password = wildestdreams
    query = 'SELECT * FROM person WHERE username = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    #stores results in var
    data = cursor.fetchone()
    cursor.close()

    if(data):
        #session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('main', username=session['username']))
    else:
        error = "Invalid login or username/password"
        return render_template('login.html', error=error)
