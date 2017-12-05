from flask import send_from_directory, render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main, time, datetime, os
from werkzeug.utils import secure_filename
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from appdef import app

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/posts_pic'
configure_uploads(app, photos)

@app.route('/posts')
def posts():
    query = "SELECT * FROM content WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('posts.html', data=data)

@app.route('/sharePost')
def sharePosts():
    query = "SELECT * FROM content WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('sharePosts.html', data=data)

@app.route('/sharingPost')
def sharingPosts():
    post_id = request.form['post_id']
    group = request.form['group']
    query = "INSERT INTO share (id, group_name, username) VALUES \
                (%s, %s, %s)"
    

@app.route('/makePost/', methods=['GET', 'POST'])
def makePost():
    return render_template('makePost.html')

@app.route('/makePost/processing', methods=['GET', 'POST'])
def makePostProcessed():
    content_name = request.form['content_name']
    public = request.form['public']
    #add code for if no selected request, make public = 0 - make the form a check as well

    img_filepath = '/static/posts_pic/'

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        img_filepath = img_filepath + filename

    username = session['username']
    cursor = conn.cursor()
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'SELECT max(id) as postID FROM Content' #to get the id of this post
    cursor.execute(query)
    postID = cursor.fetchone()['postID'] + 1
    query = 'INSERT into Content (id, username, timest, file_path, content_name, public) values (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (postID, username, timest, img_filepath, content_name, public))

    #If the content item is private, PriCoSha gives the user a way to designate
    #FriendGroups (that the user owns) with which the Photo is shared.

    if (public == '0'): #need to know which friendgroup to share it with if not public
        group_name = request.form['friend_group_name']
        query = 'INSERT into share (id, group_name, username) values (%s, %s, %s)'
        cursor.execute(query, (postID, group_name, username))

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
    cursor = conn.cursor()
    query = 'SELECT DISTINCT username FROM content WHERE content.id = %s'
    cursor.execute(query, (post_id))
    ownerOfPost = cursor.fetchone()['username']
    if ownerOfPost != username_tagger:
        flash('You cannot tag this post!')
        return redirect(url_for('main'))
    else:
        timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
        query = 'INSERT into tag (id, username_tagger, username_taggee, timest, status) values (%s, %s, %s, %s, %s)'
        cursor.execute(query, (post_id, username_tagger, username_taggee, timest, 0))
        conn.commit()
        cursor.close()
        return redirect(url_for('main'))
