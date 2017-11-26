from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags

@app.route('/')
def main():


    if (session.get('logged_in') == True):

        # get all the posts
        # postQuery = 'SELECT * FROM CONTENT WHERE username in (SELECT username FROM member WHERE username_creator="ml4963") OR username in (SELECT username FROM member WHERE group_name in (SELECT group_name FROM member WHERE member.username ="ml4963") AND username != "ml4963") OR username in (SELECT username_creator FROM member WHERE username ="ml4963") GROUP BY timest ASC'
        postQuery = 'SELECT content.id, content.username, content.timest, content.file_path, content.content_name FROM CONTENT WHERE content.public = 1 OR username in (SELECT username FROM member WHERE username = %s) OR username in (SELECT username FROM member WHERE group_name in (SELECT group_name FROM member WHERE member.username = %s)) OR username in (SELECT username_creator FROM member WHERE username = %s) ORDER BY timest DSC'
        cursor = conn.cursor()
        username = session['username']
        cursor.execute(postQuery, (username, username, username))
        postData = cursor.fetchall()
        cursor.close()

        #postData = getData(postQuery)

        # get all the tags
        tagsQuery = 'SELECT * FROM tag WHERE status = 1'
        tagsData = getData(tagsQuery)

        # get comments for posts
        commentsQuery = 'SELECT * FROM comment'
        commentsData = getData(commentsQuery)

        return render_template("index.html", data=postData, tagsData=tagsData, commentsData=commentsData)

    return render_template("index.html")

def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return(data)
