from flask import send_from_directory, render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main, time, datetime, os
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from appdef import app

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/posts_pic'
configure_uploads(app, photos)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/posts')
def posts():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    query = "SELECT * FROM content WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('posts.html', data=data)

@app.route('/sharePost')
def sharePosts():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    query = "SELECT * FROM content WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('sharePosts.html', data=data)

@app.route('/sharingPost')
def sharingPosts():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    post_id = request.form['post_id']
    group = request.form['group']
    query = "INSERT INTO share (id, group_name, username) VALUES \
                (%s, %s, %s)"

@app.route('/makePost/')
def makePost():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    return render_template('makePost.html')

@app.route('/makePost/processing', methods=['GET', 'POST'])
def makePostProcessed():

    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    content_name = request.form['content_name']
    public = request.form['public']

    img_filepath = '/static/posts_pic/'

    filenameTest = photos.url(request.files['photo'])

    if not allowed_file(request.files['photo'].filename):
        error = 'Please attach image files only.'
        return render_template('makePost.html', error=error)

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        img_filepath = img_filepath + filename


    # checks if group exists
    query = 'SELECT group_name FROM friendgroup'
    groups = getData(query)
    present = False
    for group in groups:
        if (group['group_name'] == request.form['friend_group_name']):
            present = True

    if (present == False):
        error = "Group does not exist."
        return render_template('makePost.html', error=error)

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
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    return render_template('tagUser.html', post_id = post_id)

@app.route('/tagUser/processing-<post_id>', methods=['GET', 'POST'])
def tagUserProcessed(post_id):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    username_taggee = request.form['username_taggee']

    username_tagger = session['username']
    cursor = conn.cursor()

    query = "SELECT DISTINCT content.id FROM content WHERE content.public = 1\
    OR content.username = %s OR username in(SELECT username FROM person\
    NATURAL JOIN friendgroup)"
    cursor.execute(query, (username_taggee))
    visiblePosts = cursor.fetchall() #posts visible to the taggee

    query = 'SELECT share.id FROM share WHERE %s in (SELECT member.username\
    FROM member WHERE share.group_name = member.group_name) OR (SELECT username\
    FROM friendgroup WHERE share.group_name = friendgroup.group_name)'
    cursor.execute(query, (username_taggee))
    visiblePostsShared = cursor.fetchall() #posts shared to the groups this person is in

    if post_id not in visiblePosts or visiblePostsShared:
        errormsg = "Cannot tag: post is not visible to this person!" #how to display this error msg
        return redirect(url_for('main'))

    #else if username_taggee is not in
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'INSERT into tag (id, username_tagger, username_taggee, timest, status) values (%s, %s, %s, %s, %s)'
    cursor.execute(query, (post_id, username_tagger, username_taggee, timest, 0))
    conn.commit()
    cursor.close()
    return redirect(url_for('main'))

def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data
