from flask import Flask, render_template, url_for, flash, redirect, request
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

#!------------------------------------------------------------------
import geocoder
g = geocoder.ip('me')
latitude = g.latlng[0]
longitude = g.latlng[1]
location = str(str(latitude) + str(longitude))
#!------------------------------------------------------------------


@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', title= 'About')
#!------------------------------------------------------------------

@app.route("/about")
def about():
	return render_template('about.html')
#!------------------------------------------------------------------

@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, school = form.school.data, college = form.college.data, company1 = form.company1.data, company2 = form.company2.data, gps = location, password= hashed_password)
		
		db.session.add(user)
		db.session.commit()

		flash(f'Your account has been created', 'success')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=form)
#!------------------------------------------------------------------

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		
		user = User.query.filter_by(username = form.username.data).first()
		
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user,remember = form.remember.data)
			flash('Login successful','success')
			return redirect(url_for('home'))
		
		else:
			flash('Login Unsuccessful','danger')
			
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account")
@login_required 
def account():
	return render_template('account.html', title='Account')
