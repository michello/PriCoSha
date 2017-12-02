from flask import session
from appdef import app, conn

def getFriend():

    userList = []

    # query for getting the members of the group of
    # which the username is creator of
    creatorQuery = "SELECT username, group_name \
                FROM member \
                WHERE username_creator = %s;"
    cursor = conn.cursor()
    cursor.execute(creatorQuery, (session['username']))
    userList.extend(cursor.fetchall())
    cursor.close()

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
    userList.extend(cursor.fetchall())
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
    cursor = conn.cursor()
    cursor.execute(friendCreatorQuery, (session['username']))
    userList.extend(cursor.fetchall())
    cursor.close()

    return userList
