from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, content_edit_delete, friends, group, post_tag, time, datetime, os
import getfriends, post_tag
from post_tag import makePost

@app.route('/reply-<post_id>')
def replyPost(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    
    query = 'SELECT * \
            FROM content \
            WHERE id =%s'
    cursor = conn.cursor()
    cursor.execute(query, (post_id))
    data = cursor.fetchall()
    cursor.close()

    #check if post_id even exists, otherwise return error
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM content WHERE id = %s'
    cursor.execute(query, (post_id))
    countData = cursor.fetchone()
    cursor.close()

    if (countData['COUNT(*)'] > 0):
        return render_template("reply_post.html", post_id=post_id, countData=countData, data=data)
    else:
        error = "Post does not exist. Please comment on a valid post."
        return render_template("reply_post.html", post_id=post_id, error=error, data=data)
    
@app.route('/replying-<post_id>', methods=['GET', 'POST'])
def replyingPost(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    #check if post_id even exists, otherwise return error   
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM content WHERE id = %s'
    cursor.execute(query, (post_id))
    countData = cursor.fetchone()
    cursor.close()

    if (countData['COUNT(*)'] > 0):
        return render_template("reply_post.html", post_id=post_id, countData=countData)
    else:
        error = "Post does not exist. Please comment on a valid post."
        return render_template("reply_post.html", post_id=post_id, error=error)

    content = request.form['description']
    time = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'INSERT INTO comment (id, username, timest, comment_text) VALUES (%s, %s, %s, %s)'
    cursor = conn.cursor()
    cursor.execute(query, (post_id, session['username'], time, content))
    data = conn.commit()
    cursor.close()

    return redirect(url_for('main'))
