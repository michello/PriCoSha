from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, content_edit_delete, friends, group, post_tag
import getfriends

@app.route('/')
def main():
    # if the user is logged in, have all the posts available to the user display
    if (session.get('logged_in') == True):
        # query to get all the posts available to the user
        postQuery = 'SELECT content.id, content.username, content.timest, content.file_path, content.content_name \
                    FROM CONTENT \
                    WHERE content.public = 1 \
                        OR username = %s \
                        OR username in (SELECT username \
                                        FROM member \
                                        WHERE group_name in \
                                        (SELECT group_name \
                                        FROM member \
                                        WHERE member.username = %s)) \
                        OR username in (SELECT username_creator \
                                        FROM member \
                                        WHERE username = %s) \
                        OR username in (SELECT username \
                                        FROM member \
                                        WHERE username_creator=%s) \
                    ORDER BY timest DESC'

        cursor = conn.cursor()
        username = session['username']
        cursor.execute(postQuery, (username, username, username, username))
        postData = cursor.fetchall()
        cursor.close()

        # get all the tags
        tagsQuery = 'SELECT * FROM tag WHERE status = 1'
        tagsData = getData(tagsQuery)

        # get comments for posts
        commentsQuery = 'SELECT * FROM comment'
        commentsData = getData(commentsQuery)

        # get all the users
        userQuery = 'SELECT username, first_name, last_name FROM person'
        userData = getData(userQuery)

        storeUsers(userData)

        return render_template("index.html", data=postData, tagsData=tagsData, commentsData=commentsData, userData=userData)
    return render_template("index.html")

# function to make queries to database to acquire info
def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return(data)

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
        session['users'][user['username']]['friends'] = getfriends.getFriend()

        # including groups you own
        session['users'][user['username']]['groups'] = []
        addGroups(session['users'][user['username']]['groups'])
    return;

def addGroups(groupList):
    friendGroup = "SELECT group_name, description \
                    FROM friendgroup \
                    WHERE username = %s"
    cursor = conn.cursor()
    cursor.execute(friendGroup, (session['username']))
    groupList.extend(cursor.fetchall())
    cursor.close()
