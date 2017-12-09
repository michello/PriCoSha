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

    if not allowed_file(request.files['photo'].filename):
        error = 'Please attach image files only.'
        return render_template('makePost.html', error=error)

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        img_filepath = img_filepath + filename

    if len(content_name) > 50:
        error = 'Description is too long. 50 characters max.'
        return render_template('makePost.html', error=error)
    
    # checks if group exists
    query = 'SELECT group_name FROM friendgroup'
    groups = getData(query)
    present = False
    for group in groups:
        if (group['group_name'] == request.form['friend_group_name']):
            present = True

    if (present == False and public == '0'):
        error = "Group does not exist."
        return render_template('makePost.html', error=error)

    username = session['username']
    cursor = conn.cursor()
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'SELECT max(id) as postID FROM Content' #to get the id of this post
    cursor.execute(query)
    postID = cursor.fetchone()['postID'] + 1

    #If the content item is private, PriCoSha gives the user a way to designate
    #FriendGroups (that the user owns) with which the Photo is shared.
    if (public == '1'):
        query = 'INSERT into Content (id, username, timest, file_path, content_name, public) values (%s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (postID, username, timest, img_filepath, content_name, public))
    
    if (public == '0'): #need to know which friendgroup to share it with if not public
        group_name = request.form['friend_group_name']
        #this is for if the poster is attempting to share a post to a group they are not in
        query = '(SELECT username FROM member WHERE group_name = %s) UNION\
                (SELECT username FROM friendgroup WHERE group_name = %s)'
        cursor.execute(query, (group_name, group_name))
        listPeople = cursor.fetchall() #list of people who can see that post
        #return render_template('result.html', data=listPeople)
        flag = False
        for mem in listPeople:
            if mem['username'] == username:
                flag = True
        if flag == False:
            error = "You cannot post to this group."
            return render_template('makePost.html', error=error)
        query = 'INSERT into Content (id, username, timest, file_path, content_name, public) values (%s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (postID, username, timest, img_filepath, content_name, public))
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
    #gets all the ids of the visible posts to the taggee
    query = 'SELECT content.id\
                    FROM content\
                    WHERE content.public = 1\
                    OR content.username= %s\
                    OR id in\
                    (SELECT share.id\
                    FROM share\
                    WHERE %s in\
                    (SELECT member.username\
                    FROM member\
                    WHERE share.group_name = member.group_name)\
                    OR %s in (SELECT username\
                    FROM friendgroup\
                    WHERE share.group_name = friendgroup.group_name))'
    
    cursor.execute(query, (username_taggee, username_taggee, username_taggee))
    visiblePosts = cursor.fetchall() #posts shared to the groups this person is in
    #return render_template('result.html', data=visiblePosts)
    #visiblePosts = [{'id': 3}, {'id': 5}, {'id': 7}, {'id': 9}]
    flag = False
    for mem in visiblePosts:
        if mem['id'] == int(post_id):
            flag = True

    if not flag:
        errormsg = "Cannot tag: post is not visible to this person!"
        return render_template('tagUser.html', post_id=post_id, error=errormsg)

    #checks if tag is a duplicate
    queryDuplicate = 'SELECT * FROM tag WHERE id = %s AND username_tagger = %s AND username_taggee = %s'
    cursor.execute(queryDuplicate, (post_id, username_tagger, username_taggee))
    duplicate = cursor.fetchone()
    #return render_template('result.html', data=duplicate)

    if duplicate:
        error = "Cannot tag this person: this tag already exists."
        return render_template('tagUser.html', post_id=post_id, error=error)
        
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'INSERT into tag (id, username_tagger, username_taggee, timest, status) values (%s, %s, %s, %s, %s)'

    #if user is tagging themselves ****doesnt work yet - problem may be with the two sql queries up there****
    if username_taggee == username_tagger:
        cursor.execute(query, (post_id, username_tagger, username_taggee, timest, 1))
    elif username_taggee != username_tagger:
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
