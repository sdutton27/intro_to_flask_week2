from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

# class SignUpForm(FlaskForm):
#     # behind the scenes, this converts this into fields for HTML
#     # specify the type, create instances of those types
#         # Type(the label that will show up, validators)
#                                             # how do we want to Validate the fields of a form
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])               # make sure password is filled in
#                                                                                     # the above password is a class, so the '' makes it a string
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Submit')

# class LoginForm(FlaskForm):
#     # behind the scenes, this converts this into fields for HTML
#     # specify the type, create instances of those types
#         # Type(the label that will show up, validators)
#                                             # how do we want to Validate the fields of a form
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])               # make sure password is filled in
#     submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    caption = StringField('Caption')              # make sure password is filled in
    submit = SubmitField('Submit')