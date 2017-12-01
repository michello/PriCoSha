from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

@app.route('/friends')
def friends():

    # gotta update this data every time someone successfully adds a user
    data = session['users'][session['username']]['friends']

    return render_template('friends.html', data=data)

@app.route('/addFriends')
def addFriends():
  groupQuery = 'SELECT * FROM `friendgroup` WHERE username = %s'
  group = getData(groupQuery, session['username'])
  return render_template('addFriends.html', data=group)

@app.route('/addingFriends', methods=['GET', 'POST'])
def addingFriends():

    group = request.form['group']
    fullname = request.form['name']
    first_name = ""
    last_name = ""

    # checks if username field is filled
    # username field is filled only if there
    # are two people with the same first and last name
    username = request.form.get('username', None)

    # if user entered a proper first name and last name
    if len(fullname.split()) == 2:
        first_name = fullname.split()[0]
        last_name = fullname.split()[1]
    else:
        error = "Please enter a first name and a last name."
        return render_template('addFriends.html', error=error)

    # if the username parameter is not filled, check for the username
    # with the person's first and last name
    if (username is None):

        # finding username with the entered first and last name
        cursor = conn.cursor()
        query = "SELECT username \
                    FROM person \
                    WHERE first_name = %s \
                    AND last_name = %s"
        cursor.execute(query, (first_name, last_name))
        data = cursor.fetchall()
        cursor.close()
        # return render_template('result.html', data=data)

        # if there are multiple users with the same first and last name
        if (len(data) > 1):
            error = "Please include a username."
            return render_template('addFriends.html', error=error)
        # if the user cannot be found
        elif (len(data) < 1):
            error = "User not found."
            return render_template('addFriends.html', error=error)
        else:
             query = "INSERT INTO member (username, group_name, username_creator) VALUES (%s, %s, %s)"
             cursor = conn.cursor()
             cursor.execute(query, (data['username'], group, session['username']))
             cursor.close()
             return render_template('addFriends.html')

    else:

        query = "SELECT username \
                FROM person \
                WHERE username = %s"
        cursor = conn.cursor()
        cursor.execute(query, (username))
        data = cursor.fetch.all()
        cursor.close()
        # if the username is collected
        if (data):
            query = "INSERT INTO member (username, group_name, username_creator) VALUES (%s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(query, (data['username'], group, session['username']))
            cursor.close()
            return redirect(url_for('friends'))
        else:
            error = "Username was not found. Please enter a valid one."
            return render_template('addFriends.html', error=error)
    return render_template('addFriends.html')

def getData(query, param):
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return data
