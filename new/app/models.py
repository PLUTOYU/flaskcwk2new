from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(64))

    #location=db.Column(db.String(64))
    gender=db.Column(db.Integer)
    about_me=db.Column(db.String(150))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_seen=db.Column(db.DateTime, default=datetime.utcnow())

    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    following = db.relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers'
    )

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        return 'Password is read only'

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_following(self, user):
        return self.following.filter(user_following.c.followed_id == user.id).all()


user_following = db.Table(
    'user_following', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey(User.id), primary_key=True)
)


class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    created_on = db.Column(db.DateTime, server_default=func.now())
    code = db.Column(db.String(16))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    summary = db.Column(db.String(512))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, server_default=func.now())
    comments = db.relationship('Comment', backref='post', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, server_default=func.now())
    text = db.Column(db.String(256))

# follow = db.Table('follow', db.Model.metadata,
#     db.Column('studentId', db.Integer, db.ForeignKey('student.studentId')),
#     db.Column('moduleCode', db.Integer, db.ForeignKey('module.moduleCode'))
# )
#
#
# class Student (db.Model):
#     studentId = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(250), index=True)
#     surname = db.Column(db.String(250),index=True)
#     year = db.Column(db.Date)
#     modules = db.relationship('Module',secondary=enrollment)
#     def __repr__(self):
#         return  self.firstname + ' ' + self.surname
#
# class Module (db.Model):
#     moduleCode = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(250), index=True)
#     students = db.relationship('Student',secondary=enrollment)
#     moduleLeader = db.Column(db.Integer, db.ForeignKey('staff.id'))
#
#     def __repr__(self):
#         return  self.title
#
# class Staff (db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(250), index=True)
#     surname = db.Column(db.String(250), index=True)
#     title = db.Column(db.String(10), index=True)
#     modules = db.relationship('Module', backref='staff', lazy='dynamic')
#
#     def __repr__(self):
#         return self.title + " " + self.firstname + " " + self.surname
