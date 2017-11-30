from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/addFriends')
def addFriends():
  groupQuery = 'SELECT * FROM `friendgroup` WHERE username = %s'
