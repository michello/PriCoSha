from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn
import getfriends

@app.route('/groups')
def groups():

    data = {}
    command = 'SELECT * \
                FROM friendgroup \
                WHERE username = %s'
    data['owner'] = getData(command, session['username'])

    command = 'SELECT member.username, member.group_name, friendgroup.description \
                FROM member \
                INNER JOIN friendgroup \
                WHERE member.username = %s \
                GROUP BY member.group_name'
    data['member'] = getData(command, session['username'])

    return render_template('groups.html', data=data)

@app.route('/delete-group-<group_name>')
def deleteGroups(group_name):
    # delete all the members in the group first
    command = 'DELETE FROM member \
                WHERE group_name = %s;'
    execute(command, group_name)
    # then delete the group itself
    command = 'DELETE FROM friendgroup \
                WHERE group_name=%s;'
    execute(command, group_name)

    return redirect(url_for('groups'))

@app.route('/leave-group-<group_name>')
def leaveGroups(group_name):
    command = "DELETE FROM member \
                WHERE group_name = %s AND username="+ "'" + session['username'] + "'"
    execute(command, group_name)
    return redirect(url_for('groups'))

def getData(query, param):
    cursor = conn.cursor()
    cursor.execute(query, (param))
    data = cursor.fetchall()
    cursor.close()
    return data

def execute(query, param):
    cursor = conn.cursor()
    cursor.execute(query, (param))
    conn.commit()
    cursor.close()
    return;
