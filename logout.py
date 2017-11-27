from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/logout')
def logout():
    # logs user out of current session
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('main'))
