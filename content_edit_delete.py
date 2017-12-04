from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main

@app.route('/edit-post/<post_id>')
def editPost(post_id):
    return render_template("content_edit.html", post_id=post_id)

@app.route('/edit-post/processing-<post_id>', methods=['GET', 'POST'])
def editPostProcessed(post_id):
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
                   WHERE content.id = %s'

    cursor.execute(updateQuery, (filepath, postContent, pubOrPriv, post_id))
    conn.commit()
    cursor.close()

    return redirect(url_for('main'))

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

#likes a post via INSERT into likes table, and then redirect to homepage
@app.route('/like-post/<post_id>')
def likePost(post_id):
    cursor = conn.cursor()
    likePostQuery = 'INSERT INTO likes (id, username_liker) VALUES ('+post_id+', "'+session['username']+'")'

    cursor.execute(likePostQuery)
    conn.commit()
    cursor.close()

    return redirect(url_for('main'))

@app.route('/unlike-post/<post_id>')
def dislikePost(post_id):
    cursor = conn.cursor()
    dislikePostQuery = 'DELETE FROM likes WHERE username_liker="'+session['username']+'" AND id='+post_id

    cursor.execute(dislikePostQuery)
    conn.commit()
    cursor.close()

    return redirect(url_for('main'))




