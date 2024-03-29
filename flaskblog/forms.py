from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user
#!----------------------------------------------------------------------------------------------------------

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(max=20)])
	# name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	college = StringField('College')
	school = StringField('School', validators=[Length(max=50)])
	company1 = StringField('Company1', validators=[Length(max=50)])
	company2 = StringField('Company2', validators=[Length(max=50)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	
	submit= SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user :
			raise ValidationError('Username Already Exists')
	
	def validate_email(self, email):
		email = User.query.filter_by(email = email.data).first()
		if email :
			raise ValidationError('Email already taken')
	

#!----------------------------------------------------------------------------------------------------------

class LoginForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit= SubmitField('Login')
	remember = BooleanField('Remember Me')
#!----------------------------------------------------------------------------------------------------------

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	# name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	college = StringField('College')
	school = StringField('School', validators=[Length(min=5, max=50)])
	company1 = StringField('Company1', validators=[Length(max=50)])
	company2 = StringField('Company2', validators=[Length(max=50)])
	
	submit= SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user :
				raise ValidationError('Username Already Exists')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email = email.data).first()
			if email :
				raise ValidationError('Email already taken')

	


			

