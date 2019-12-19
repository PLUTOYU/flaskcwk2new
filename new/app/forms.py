from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
from wtforms import StringField, PasswordField,DateField,SelectField
from wtforms.validators import DataRequired, ValidationError,Length,EqualTo

from .models import User, VerificationCode


class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()], render_kw={'placeholder': 'Email Address'})
    code = StringField('code', validators=[DataRequired()], render_kw={'placeholder': 'Email Verification Code'})
    username = StringField('username', validators=[DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email has been registered')
        return email

    def validate_code(self, code):
        vc = VerificationCode.query.filter_by(email=self.email.data).order_by(VerificationCode.created_on.desc())
        if vc and vc[-1].code == code.data:
            return code
        raise ValidationError('Verification code error')


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()], render_kw={'placeholder': 'Email Address'})
    password = PasswordField('password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})

    def validate_email(self, email):
        user = User.query.filter_by(email=email)
        if not user:
            raise ValidationError('The email has not been registered yet.')
        return email

class EiditPersonalForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    #year = DateField('year', validators=[DataRequired()])
    discription = StringField('about_me', validators=[DataRequired()])
    gender = SelectField('gender', choices=[(1, 'man'), (2, 'woman')],validators=[DataRequired()],default=1,coerce=int)


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('old password', validators=[DataRequired(),Length(min=1, max=3, message="too short")], render_kw={'placeholder': 'Old Password'})
    new_password = PasswordField('new password', validators=[DataRequired(),Length(min=1, max=3, message="too short")], render_kw={'placeholder': 'New Password'})


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()], render_kw={'placeholder': 'Post title'})
    summary = StringField('summary', validators=[DataRequired()], render_kw={'placeholder': 'Post Summary'})
    content = StringField('content', validators=[DataRequired()], widget=TextArea(), render_kw={'placeholder': 'Post content'})


class CommentForm(FlaskForm):
    text = StringField('comment', validators=[DataRequired()], render_kw={'placeholder': 'Post Comment'})