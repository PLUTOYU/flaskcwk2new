import random
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from . import auth
from app.flask_logging import logger
from flask_cors import cross_origin
from app.tasks import send_async_email
from app.models import db, User, VerificationCode
from app.forms import RegisterForm, LoginForm, ChangePasswordForm


#reset the user login in time
#@auth.before_app_request
#def before_request():
#    user = User.query.filter_by(id=session['user_id']).first()
#    user.ping()

#initial form and get form's data for register the new user
@auth.route('/register', methods=['GET', 'POST'])
def register():
    #logger.info('info log')
    #logger.debug('debug log')
    #logger.warning('warning log')
    #logger.error('error log')
    #logger.critical('critical')
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():   #如果一个人重复提交多个send邮件则不行
        user = User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        logger.info(f'{user.username} registration success.')
        flash('User registered successfully.', 'alert-success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

#send the email to input email to vilidation by celery excute the tasks then
#store the code and email to the verification model for testing
@auth.route('/verification', methods=['GET'])
@cross_origin()
def verification():
    email = request.args.get('email')
    code = ''.join(map(str, random.choices(range(9), k=4)))
    email_data = {
        'to': email,
        'subject': 'Verify your email address',
        'body': 'email/confirm',

    }
    send_async_email.delay(email_data,code=code)
    flash('Verification code sent.', 'alert-success')
    vc = VerificationCode(email=email, code=code, created_on=datetime.datetime.now())
    db.session.add(vc)
    return 'ok'

#
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            flash('login successful.', 'alert-success')
            session['username'] = user.username
            session['user_id'] = user.id
            logger.info(f'{user.username} login success.')
            #有时间可以改成钩子函数！改变这个最后时间的
            return redirect(url_for('index'))
        if user is None:
            flash('input none email address.', 'alert-danger')
            return redirect(url_for('auth.login'))
        logger.error(f'{user.username} input the wrong password.')#这里不能像日志文件中输入错误的信息
        flash('Wrong password.', 'alert-danger')
    return render_template('login.html', form=form)



@auth.route('/logout')
def logout():
    user_log = User.query.filter_by(id=session['user_id']).first()
    user_log.last_seen = datetime.datetime.now()
    db.session.add(user_log)
    db.session.commit()
    logger.info(f'user {session["username"]} logout.')
    session['username'] = ''
    session['user_id'] = ''
    flash('User has logged out', 'alert-success')
    return redirect(url_for('auth.login'))



@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    logger.warning(f'{session["username"]} change password.')
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(id=session['user_id']).first()
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            flash('change password success', 'alert-success')
            return redirect('auth.logout')
        flash('wrong old password', 'alert-danger')
    return render_template('change_password.html', form=form)


