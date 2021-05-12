#this is where we structure the form using wtfors
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

class UserInfoForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField()
