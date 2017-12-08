from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/tags')
def tags():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    # making an sql query to obtain tag requests that the user has yet
    # to approve (when status = 0)
    cursor = conn.cursor()
    query = 'SELECT * FROM tag WHERE username_taggee = %s and status = 0'
    cursor.execute(query, (session['username']))
    dataTwo = cursor.fetchall()
    cursor.close()
    #return render_template("result.html", data=data)
    request_id = {}
    for item in dataTwo:
        post_id = int(item['id'])
        cursor = conn.cursor()
        query = 'SELECT file_path FROM content WHERE id = %s'
        cursor.execute(query, (post_id))
        data = cursor.fetchall()
        cursor.close()
        request_id[post_id] = ""
        request_id[post_id] = data[0]['file_path']

    #return render_template("result.html", data=request_id)
    return render_template("tags.html", data=dataTwo, request_id=request_id)


@app.route('/proccessTags', methods=['GET', 'POST'])
def proccessTags():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    # obtains all the info from the form fields (which is used to allow user to
    # accept or reject tag requests)
    data = request.form
    post = list(request.form.keys())[0]
    choice = data[post]
    user = session['username']

    # if user approves, make a query to database that updates the tag request
    # status to true
    if (choice == "True"):
        query = 'UPDATE tag SET status = 1 WHERE id =%s AND username_taggee =%s'
    # if user does not approve, delete the tag request from the database
    else:
        query = 'DELETE FROM tag WHERE id =%s AND username_taggee=%s'
    executeQuery(query, post, user)
    return redirect(url_for('tags'))


def executeQuery(command, post, user):

    cursor = conn.cursor()
    cursor.execute(command, (post, user))
    cursor.close()
