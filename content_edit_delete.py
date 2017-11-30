from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main

@app.route('/edit-post/<post_id>')
def editPost(post_id):
    return render_template("content_edit.html")

@app.route('/edit-post/processing')
def editPostProcessed():
    filepath = request.form['filepath']
    postContent = request.form['content']
    pubOrPriv = request.form['publicity']

    # conducts queries to update post
    cursor = conn.cursor()
    updateQuery = 'UPDATE * FROM content WHERE file_path = %s AND content_name = %s AND public = %s AND timest = CURRENT_TIMESTAMP'
    cursor.execute(updateQuery, (username, password))
    data = cursor.fetchone()
    cursor.close()
    
    return render_template('index.html')

#deletes a post and redirects to indicate the post was deleted
@app.route('/delete-post/<post_id>')
def deletePost(post_id):
    cursor = conn.cursor()
    deleteQuery = 'DELETE FROM content WHERE content.id = '+post_id
    cursor.execute(deleteQuery)
    cursor.close()
    return render_template('content_delete.html', post_id=post_id)
