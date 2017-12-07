from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import tags, main

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/posts_pic'
configure_uploads(app, photos)

@app.route('/edit-post/<post_id>')
def editPost(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    cursor = conn.cursor()
    query = 'SELECT * FROM content WHERE id = %s'
    cursor.execute(query, (post_id))
    data = cursor.fetchall()
    cursor.close()

    #checks if there is a post with the given post_id, spit out error otherwise
    cursor = conn.cursor()
    editCountQuery = 'SELECT COUNT(*) FROM content WHERE id = %s'
    cursor.execute(editCountQuery, (post_id))
    countData = cursor.fetchone()
    cursor.close()
        
    if (countData['COUNT(*)'] > 0):
        return render_template("content_edit.html", post_id=post_id, data=data, countData=countData)
    else:
        editError = "Post ID does not exist. Please edit a valid post."
        return render_template("content_edit.html", post_id=post_id, data=data, editError=editError)

@app.route('/edit-post/processing-<post_id>', methods=['GET', 'POST'])
def editPostProcessed(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    postContent = request.form['content']
    pubOrPriv = request.form['publicity']

    img_filepath = '/static/posts_pic/'

    #checks for image files, spits error if not
    if request.method == 'POST' and request.files['photo'].filename:
        filenameTest = photos.url(request.files['photo'])
        if (filenameTest.find('.jpg') == -1) or (filenameTest.find('.png') == -1) or (filenameTest.find('.jpeg') == -1) or (filenameTest.find('.JPG') == -1) or (filenameTest.find('.JPEG') == -1):
            error = 'Please attach image files only.'
            return render_template('content_edit.html', post_id=post_id, error=error)

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        img_filepath = img_filepath + filename

    # conducts queries to update post
    cursor = conn.cursor()
    updateQuery = 'UPDATE content \
                   SET \
                        file_path = %s, \
                        content_name = %s, \
                        public = %s, \
                        timest = CURRENT_TIMESTAMP \
                   WHERE content.id = %s'

    cursor.execute(updateQuery, (img_filepath, postContent, pubOrPriv, post_id))
    conn.commit()
    cursor.close()

    return redirect(url_for('main'))

#deletes a post and redirects to indicate the post was deleted
@app.route('/delete-post/<post_id>')
def deletePost(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    userQuery = 'SELECT username FROM share WHERE id = %s'
    user = getData(userQuery, post_id)

    if (user != session['username']):
        return redirect(url_for('main'))
    else:
        # check if post is in table
        shareQuery = 'SELECT * FROM share WHERE id = %s'
        data = getData(shareQuery, post_id)

        if (data != []):
            delete = 'DELETE FROM share WHERE id = %s'
            cursor = conn.cursor()
            cursor.execute(delete, (post_id))
            conn.commit() #commit the change to DB
            cursor.close()

        cursor = conn.cursor()
        #two delete queries; must delete tag because foreign key constraint
        deleteQuery = 'DELETE FROM tag WHERE tag.id='+post_id+'; DELETE FROM likes WHERE likes.id='+post_id+'; DELETE FROM content WHERE content.id = '+post_id
        cursor.execute(deleteQuery)
        conn.commit() #commit the change to DB
        cursor.close()


    return render_template('content_delete.html', post_id=post_id)


#likes a post via INSERT into likes table, and then redirect to homepage
@app.route('/like-post/<post_id>')
def likePost(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    cursor = conn.cursor()
    likePostQuery = 'INSERT INTO likes (id, username_liker) VALUES ('+post_id+', "'+session['username']+'")'

    cursor.execute(likePostQuery)
    conn.commit()
    cursor.close()

    return redirect(url_for('main'))

@app.route('/unlike-post/<post_id>')
def dislikePost(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    cursor = conn.cursor()
    dislikePostQuery = 'DELETE FROM likes WHERE username_liker="'+session['username']+'" AND id='+post_id
    cursor.execute(dislikePostQuery)
    conn.commit()
    cursor.close()

    return redirect(url_for('main'))

def getData(query, item):
    cursor = conn.cursor()
    cursor.execute(query, (item))
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    return data
