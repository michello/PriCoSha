from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn

@app.route('/profile/<username>')
def profile(username):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    data = getInfo(username)
    if data is None:
        error = "User does not exist."
        return render_template('profile.html', username="error", error=error)

    return render_template('profile.html', username=username, data=data)

@app.route('/profile/edit-<username>')
def editProfile(username):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    return render_template('editProfile.html', username=username)

def getInfo(username):
    query = "SELECT * FROM profile WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    return(data)
