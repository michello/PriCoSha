from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app

@app.route('/login')
def login():
    return render_template('login.html')

# authenticates logins
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	username = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()