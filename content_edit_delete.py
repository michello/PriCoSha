from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main

global_post_id = ''

@app.route('/edit-post/<post_id>')
def editPost(post_id):
    global_post_id = post_id
    return render_template("content_edit.html")

@app.route('/edit-post/processing', methods=['GET', 'POST'])
def editPostProcessed():
    filepath = request.form['filepath']
    postContent = request.form['content']
    pubOrPriv = request.form['publicity']

    # conducts queries to update post
    cursor = conn.cursor()
    updateQuery = 'UPDATE content \
                   SET \
                        file_path = %s, \
                        content_name = %s, \
                        public = %s, \
                        timest = CURRENT_TIMESTAMP \
                   WHERE content.id = '+global_post_id

    cursor.execute(updateQuery, (filepath, postContent, pubOrPriv))
    conn.commit()
    cursor.close()

    return redirect(url_for('index'))

#deletes a post and redirects to indicate the post was deleted
@app.route('/delete-post/<post_id>')
def deletePost(post_id):
    cursor = conn.cursor()
    #two delete queries; must delete tag because foreign key constraint
    deleteQuery = 'DELETE FROM tag WHERE tag.id='+post_id+'; DELETE FROM content WHERE content.id = '+post_id
    cursor.execute(deleteQuery)
    conn.commit() #commit the change to DB
    cursor.close()
    return render_template('content_delete.html', post_id=post_id)
