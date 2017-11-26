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
    data = cursor.fetchall()
    cursor.close()

    return render_template("tags.html", data=data)


@app.route('/proccessTags', methods=['GET', 'POST'])
def proccessTags():
    data = request.form
    post = list(request.form.keys())[0]
    choice = data[post]
    user = session['username']
    if (choice == "True"):
        query = 'UPDATE tag SET status = 1 WHERE id =%s AND username_taggee =%s'
    else:
        query = 'DELETE FROM tag WHERE id =%s AND username_taggee=%s'
    executeQuery(query, post, user)
    return redirect(url_for('tags'))

def executeQuery(command, post, user):
    cursor = conn.cursor()
    cursor.execute(command, (post, user))
    cursor.close()
