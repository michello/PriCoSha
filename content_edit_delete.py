from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import tags, main

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/posts_pic'
configure_uploads(app, photos)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        editError = "Post does not exist. Please edit a valid post."
        return render_template("content_edit.html", post_id=post_id, data=data, editError=editError)

@app.route('/edit-post/processing-<post_id>', methods=['GET', 'POST'])
def editPostProcessed(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    postContent = request.form['content']
    pubOrPriv = request.form['publicity']

    if (request.form['friend_group_name']):
        friendgroup = request.form['friend_group_name']
    
    img_filepath = '/static/posts_pic/'

    if not allowed_file(request.files['photo'].filename):
        error = 'Please attach image files only.'
        return render_template('content_edit.html', error=error)

    if len(postContent) > 50:
        error = 'Description is too long. 50 characters max.'
        return render_template('content_edit.html', post_id=post_id, error=error)

    if (friendgroup and len(friendgroup)) > 50:
        error = 'Friendgroup is too long. 50 characters max.'
        return render_template('content_edit.html', post_id=post_id, error=error)
   
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        img_filepath = img_filepath + filename

    # checks if group exists
    checkGroupQuery = 'SELECT group_name FROM friendgroup'
    cursor = conn.cursor()
    cursor.execute(checkGroupQuery)
    groups = cursor.fetchall()
    cursor.close()
    
    present = False
    
    for group in groups: #note groups is merely a dictionary.
        if (group['group_name'] == request.form['friend_group_name']):
            present = True

    if (present == False and pubOrPriv == '0'):
        error = "Group does not exist."
        return render_template('content_edit.html', error=error, post_id=post_id)
    
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

    userQuery = 'SELECT username FROM content WHERE id = %s'
    user = getData(userQuery, post_id)

    if (user['username'] != session['username']):
        #return render_template('result.html', data=user['username'])
        error = "This is not your post to delete!"
        return redirect(url_for('main'))
    else:
        # check if post is in table
        shareQuery = 'SELECT * FROM share WHERE id = %s'
        data = getData(shareQuery, post_id)

        if (data is not None):
            delete = 'DELETE FROM share WHERE id = %s'
            cursor = conn.cursor()
            cursor.execute(delete, (post_id))
            conn.commit() #commit the change to DB
            cursor.close()

        cursor = conn.cursor()
        #two delete queries; must delete tag because foreign key constraint
        delete = 'DELETE FROM tag WHERE tag.id=%s'
        cursor.execute(delete, (post_id))
        conn.commit() #commit the change to DB
        delete = 'DELETE FROM likes WHERE likes.id=%s'
        cursor.execute(delete, (post_id))
        conn.commit() #commit the change to DB
        delete = 'DELETE FROM comment WHERE comment.id=%s'
        cursor.execute(delete, (post_id))
        conn.commit() #commit the change to DB
        delete = 'DELETE FROM content WHERE content.id=%s'
        cursor.execute(delete, (post_id))
        conn.commit() #commit the change to DB
        cursor.close()

    return redirect(url_for('main'))
    # return render_template('content_delete.html', post_id=post_id)


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
