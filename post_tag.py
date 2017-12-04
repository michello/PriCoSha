from flask import send_from_directory, render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main, time, datetime, os
from werkzeug.utils import secure_filename
from appdef import app

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\posts_pic')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

'''
@app.route('uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config[UPLOAD_FOLDER], filename)
'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/makePost/', methods=['GET', 'POST'])
def makePost():
    return render_template('makePost.html')

@app.route('/makePost/processing', methods=['GET', 'POST'])
def makePostProcessed():
    content_name = request.form['content_name']
    public = 0 #default value is 0 (private)
    public = request.form['public']

    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static\posts_pic')
    
    uploadfile = request.files['file_path']
    if uploadfile and allowed_file(uploadfile.filename):    
        filename = (secure_filename(uploadfile.filename))
        uploadfile.save(app.config[UPLOAD_FOLDER], filename)
        #return redirect(url_for('makePostProcessed', filename=filename))
                  
    username = session['username']
    cursor = conn.cursor()
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'SELECT max(id) as postID FROM Content' #to get the id of this post
    cursor.execute(query)
    postID = cursor.fetchone()['postID']
    query = 'INSERT into Content (id, username, timest, file_path, content_name, public) values (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (postID, username, timest, uploadfile, content_name, public))

    #If the content item is private, PriCoSha gives the user a way to designate
    #FriendGroups (that the user owns) with which the Photo is shared.

    if (public == '0'): #need to know which friendgroup to share it with if not public
        group_name = request.form['friend_group_name']
        query = 'INSERT into share values(postID, friend_group_name, username) values (%s, %s, %s)'
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
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    query = 'INSERT into tag (id, username_tagger, username_taggee, timest, status) values (%s, %s, %s, %s, %s)'
    cursor.execute(query, (post_id, username_tagger, username_taggee, timest, 0))
    conn.commit()
    cursor.close()
    return redirect(url_for('main'))
