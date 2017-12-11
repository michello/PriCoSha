from flask import Flask, render_template, request, session, url_for, redirect
from appdef import app
import main, login, logout
import pymysql.cursors
from datetime import timedelta

app.secret_key = 'D7X15LEycA'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

if __name__ == "__main__":
    app.run('localhost', 5000, debug = True)
