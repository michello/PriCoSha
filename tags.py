from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/tags')
def tags():

    cursor = conn.cursor()
    # username = ml4963
    # password = wildestdreams
    query = 'SELECT * FROM tag WHERE username_taggee = %s and status = 0'
    cursor.execute(query, (session['username']))
    data = cursor.fetchone()
    cursor.close()

    return render_template("tags.html", data=data)


@app.route('/proccessTags', methods=['GET', 'POST'])
def proccessTags():
    if (request.form['choice']):
        print("Hello!")
    else:
        return redirect(url_for('tags'))
