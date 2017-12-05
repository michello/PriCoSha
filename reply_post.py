from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, content_edit_delete, friends, group, post_tag
import getfriends, post_tag
from post_tag import makePost

@app.route('/reply-<post_id>')
def replyPost(post_id):
    return render_template('reply_post.html')
