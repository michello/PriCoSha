from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main, time, datetime


@app.route('/makePost', methods=['GET', 'POST'])
def makePost():
    content_name = request.form['content_name']
    file_path = request.form['file_path']
    public = request.form['ispublic']
    
    username = session['username']
    cursor = conn.cursor()
    timest = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    "need to save the image in the static folder"
    maxID = 'SELECT max(id)+1 FROM Content'
    cursor.execute(maxID)
    query = 'INSERT into Content (maxID, username, timest, file_path, content_name, public) values (%s, %s, %s, %s, %s)'
    cursor.execute(query, (maxID, username, timest, file_path, content_name, public))

    if (public == '0'):
        friend_group_name = request.form['friendgroup']
        query = 'SELECT max(id) AS max FROM Content'
        cursor.execute(query)
        postID = cursor.fetchone()['max']
        query = '''INSERT into share VALUES( %s, %s, %s)'''
        cursor.execute(query, (postID, friend_group_name, username))
        conn.commit()
        cursor.close()
        return redirect(url_for('main'))


@app.route('/tagUser/<post_id>')
def tagUser(post_id):
    return render_template('tagUser.html', post_id = post_id)

@app.route('/tagUser/processing-<post_id>', methods=['GET', 'POST'])
def tagUserProcessed(post_id):
    username_taggee = request.form['username_taggee']
    
    username_tagger = session['username']
    timest = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    query = 'INSERT into tag (id, username_tagger, username_taggee, timest, status)'
    cursor.execute(query, (post_id, username_tagger, username_taggee, timest, 0))
    cursor.close()
    return redirect(url_for('main'))
