import datetime
from flask import request, render_template, flash, redirect, url_for, session, current_app
from app import app, db
import logging

from .models import User, Post, Comment
from .forms import PostForm, CommentForm,EiditPersonalForm
from app.flask_logging import logger

#reset the user login in time
#@app.before_request
#def before_request():
#    if current_user.is_authenticated:
#        current_user.ping()



@app.route('/', methods=['GET'])
def index(page=None):

    #if not page:
    #    page = 1
    paginate = Post.query.order_by(Post.created_on.desc()).paginate(page=page,per_page=6)
    stus = paginate.items

    return render_template('index.html',  posts=stus, paginate = paginate)

@app.route('/Blogs/<int:user_id>', methods=['GET','POST'])
def userBlog_list(user_id,page=None):
    #if not page:
    #    page = 1
    paginate = Post.query.filter_by(user_id=user_id).order_by(Post.created_on).paginate(page=page,per_page=6)
    stus = paginate.items
    user = User.query.get(user_id)
    return render_template('userblog_list.html',posts=stus, paginate = paginate,username=user)



@app.route('/<int:page>', methods=['GET'])
def index_list(page=None):
    if not page:
        page = 1
    paginate = Post.query.order_by(Post.created_on.desc()).paginate(page=page,per_page=6)
    stus = paginate.items
    return render_template('index.html', posts=stus, paginate=paginate)
        #if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
         #   return redirect(url_for('auth.unconfirmed'))

#def index():
   #posts = Post.query.all()
   # return render_template('index.html', posts=posts)

@app.route('/user<int:user_id>', methods=['GET','POST'])
def user_Page(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
   # posts = user.posts.order_by(Post.created_on.desc()).all()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_on)
    following = user.following
    followed = user.followers
    comments = Comment.query.filter_by(user_id=user_id).order_by(Comment.created_on)
    return render_template('userPage.html',user=user,current_time=datetime.datetime.now(),posts=posts,following=following,followers=followed,
                           comments=comments)

@app.route('/eidtInfo/<int:user_id>', methods=['GET','POST'])
def edit_Info(user_id):
    user = User.query.get(user_id)
    form = EiditPersonalForm(object=user)
    #print(form.gender.data)
    if request.method == 'POST' and form.validate_on_submit():
        new_info = user
        new_info.gender = form.gender.data
        new_info.username = form.username.data
        new_info.about_me = form.discription.data
        db.session.commit()
        session['username'] = new_info.username
        return redirect(url_for('user_Page',user_id=new_info.id))
    flash('error')
    return render_template('edit_userinfor.html',form=form)



@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post()
        post.title = form.title.data
        post.summary = form.summary.data
        post.content = form.content.data
        post.user_id = session['user_id']
        post.created_on = datetime.datetime.now()
        db.session.add(post)
        flash('Success', 'alert-success')
        logger.info(f'{session["username"]} create a post.')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    user = User.query.filter_by(id=session.get('user_id')).first()
    form = CommentForm(request.form)
    post = Post.query.filter_by(id=id).first()
    cid = request.args.get('cid')
    if request.method == 'POST' and form.validate():
        if cid:
            comment = Comment.query.filter_by(id=cid).first()
            comment.text = form.text.data
            db.session.commit()
            flash('Comment edited successfully', 'alert-success')
        else:
            comment = Comment()
            comment.post_id = post.id
            comment.user_id = session['user_id']
            comment.text = form.text.data
            comment.created_on = datetime.datetime.now()
            db.session.add(comment)
            logger.info(f'{session["username"]} create a comment for post {post.id}.')
            flash('Comment added successfully', 'alert-success')
        return redirect(url_for('post', id=post.id))
    if cid:
        comment = Comment.query.filter_by(id=cid).first()
        form.text.data = comment.text
    return render_template('post.html', post=post, form=form, cid=cid, user=user)


@app.route('/delete_post/<int:id>')
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    flash('Delete success', 'alert-success')
    return redirect(url_for('index'))


@app.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post.title = form.title.data
        post.summary = form.summary.data
        post.content = form.content.data
        post.user_id = session['user_id']
        db.session.commit()
        flash('Success', 'alert-success')
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.summary.data = post.summary
    form.content.data = post.content
    return render_template('edit_post.html', form=form, instance=post)


@app.route('/delete_comment/<int:id>/<int:pid>')
def delete_comment(id, pid):
    Comment.query.filter_by(id=id).delete()
    flash('Delete success', 'alert-success')
    return redirect(url_for('post', id=pid))


@app.route('/follow/<int:id>/<int:pid>')
def follow(id, pid):
    print(id, User.query.filter_by(id=session['user_id']).first().id)
    user = User.query.filter_by(id=id).first()
    follower = User.query.filter_by(id=session['user_id']).first()
    user.followers.append(follower)
    db.session.add(user)
    logger.info(f'{session["username"]} following {user.username}.')
    flash('Success', 'alert-success')
    return redirect(url_for('post', id=pid))


@app.route('/unfollow/<int:id>/<int:pid>')
def unfollow(id, pid):
    user = User.query.filter_by(id=id).first()
    follower = User.query.filter_by(id=session['user_id']).first()
    user.followers.remove(follower)
    db.session.commit()
    flash('Success', 'alert-success')
    return redirect(url_for('post', id=pid))
