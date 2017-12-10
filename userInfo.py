from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import getfriends

def initiate():
    # get all the users
    userQuery = 'SELECT username, first_name, last_name FROM person'
    userData = getData(userQuery)
    storeUsers(userData)


def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return(data)

def addGroups(groupList):
    friendGroup = "SELECT group_name, description \
                    FROM friendgroup \
                    WHERE username = %s"
    cursor = conn.cursor()
    cursor.execute(friendGroup, (session['username']))
    groupList.extend(cursor.fetchall())
    cursor.close()

def storeUsers(data):
    # store users in a session users dictionary
    # which can be used to access users' first name and last name.
    session['users'] = {}
    for user in data:
        session['users'][user['username']] = {}
        session['users'][user['username']]['first_name'] = user['first_name']
        session['users'][user['username']]['last_name'] = user['last_name']
        # adding friends for users
        session['users'][user['username']]['friends'] = []

        #session['users'][user['username']]['friends'] = getfriends.getFriend()

        # including groups you own
        session['users'][user['username']]['groups'] = []
        #addGroups(session['users'][user['username']]['groups'])
    return;
