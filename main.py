from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn

@app.route('/')
def main():
    if (session.get('logged_in') == True):
        cursor = conn.cursor()
        curr_user = session['username']
        query = 'select * from content where username in member '
        cursor.execute(query, (searchtext))
        data = cursor.fetchall()
        cursor.close()
    return render_template("index.html")
