from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import tags, main

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/posts_pic'
configure_uploads(app, photos)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile/<username>')
def profile(username):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    data = getInfo(username)
    if data is None:
        error = "User does not exist."
        return render_template('profile.html', username="error", error=error)

    return render_template('profile.html', username=username, data=data)

@app.route('/profile/edit-<username>')
def editProfile(username):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    data = getInfo(username)

    #Cannot edit another user's profile. Checks for that error.
    if (session['username'] != username):
        error = 'Cannot edit another user profile.'
        return render_template('editProfile.html', username=username, data=data, error=error)

    return render_template('editProfile.html', username=username, data=data)

@app.route('/edit-profile/processing-<username>', methods=['GET', 'POST'])
def editProfileProcessed(username):
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    #Cannot edit another user's profile. Checks for that error.
    if (session['username'] != username):
        error = 'Cannot edit another user profile.'
        return render_template('editProfile.html', username=username, error=error)

    biography = request.form['bio']

    img_filepath = '/static/posts_pic/'
    hello = request.files['photo'].filename

    data = getInfo(username)


    if (allowed_file(request.files['photo'].filename) == False):
        error = 'Please attach image files only.'
        return render_template('editProfile.html', username=username, error=error, data=data)

    return render_template('result.html', username=username, data=data)

"""
    if len(biography) > 50:
        error = 'Bio is too long. 50 characters max.'
        return render_template('editProfile.html', username=username, error=error)

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        img_filepath = img_filepath + filename

    # conducts queries to update post
    cursor = conn.cursor()
    updateQuery = 'UPDATE profile \
                   SET \
                        bio = %s, \
                        file_path = %s \
                   WHERE profile.username = %s'

    cursor.execute(updateQuery, (biography, img_filepath, username))
    conn.commit()
    cursor.close()

    return redirect(url_for('profile', username=username))
"""

def getInfo(username):
    query = "SELECT * FROM profile WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    return(data)
