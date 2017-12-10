from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn
import userInfo


@app.route('/register')
def register():
    #return render_template("result.html", data=session)
    userInfo.initiate()
    return render_template('register.html')

@app.route('/register/processing', methods=['GET', 'POST'])
def registerProcessing():
    username = request.form['username']
    if username in session['users'].keys():
        errormsg = "Username already taken."
        return render_template('register.html', error = errormsg)
    if len(username) < 4:
        errormsg = "Username is too short. Must be more than 3 characters."
        return render_template('register.html', error = errormsg)
    elif len(username) > 50:
        errormsg = "Username and/or other fields are too long. 50 characters max."
        return render_template('register.html', error = errormsg)
    password = request.form['password']
    if len(password) < 4:
        errormsg = "Password is too short (needs to be greater than 3 characters)."
        return render_template('register.html', error = errormsg)
    elif len(password) > 50:
        errormsg = "Password is too long. 50 characters max."
        return render_template('register.html', error = errormsg)
    retype = request.form['retype']
    if retype != password:
        errormsg = "Passwords do not match."
        return render_template('register.html', error = errormsg)

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    cursor = conn.cursor()
    query = 'INSERT INTO person (username, password, first_name, last_name) VALUES (%s, md5(%s), %s, %s)'
    cursor.execute(query, (username, password, firstname, lastname))
    conn.commit()
    cursor.close()

    query = "INSERT INTO profile (username, bio, file_path) VALUES (%s, '', '')"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    conn.commit()
    cursor.close()

    session['logged_in'] = True
    session['username'] = username
    session['users'][username] = {}
    session['users'][username]['groups'] = []
    session['users'][username]['first_name'] = firstname
    session['users'][username]['last_name'] = lastname
    return redirect(url_for('main', username = session['username']))
