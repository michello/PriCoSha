from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from appdef import app, conn

"""
SELECT username, group_name
FROM member
WHERE username_creator = 'ml4963';

SELECT username, group_name
FROM member
WHERE group_name in
	(SELECT group_name FROM member WHERE username = 'ml4963')
HAVING username != 'ml4963';

SELECT username_creator, group_name
FROM member
WHERE group_name in
	(SELECT group_name FROM member WHERE username = 'ml4963')
GROUP BY group_name;
"""

@app.route('/friends')
def friends():
    friends = []

    # query for getting the members of the group of
    # which the username is creator of
    creatorQuery = "SELECT username, group_name \
                FROM member \
                WHERE username_creator = %s;"
    friends.extend(getData(creatorQuery, 'ml4963'))

    # query for getting the members of the group of
    # which the username is a member of
    cursor = conn.cursor()
    memberQuery = "SELECT username, group_name \
                    FROM member \
                    WHERE group_name in \
    	               (SELECT group_name \
                       FROM member \
                       WHERE username = %s) \
                    HAVING username != %s;"
    cursor.execute(memberQuery, (session['username'], session['username']))
    friends.extend(cursor.fetchall())
    cursor.close()

    # query for getting the creators of the group of
    # which the user is a member of
    friendCreatorQuery = "SELECT username_creator, group_name \
                            FROM member \
                            WHERE group_name in \
	                           (SELECT group_name \
                               FROM member \
                               WHERE username = %s) \
                            GROUP BY group_name;"
    friends.extend(getData(friendCreatorQuery, session['username']))

    return render_template('friends.html', data=friends)


def getData(query, param):
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return data
