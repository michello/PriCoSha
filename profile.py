from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn

@app.route('/profile/<username>')
def profile(username):
    
    return render_template('profile.html', username=username)
