from flask import Flask, render_template, url_for, flash, redirect
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', title= 'About')


@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account Created for {form.username.data}', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)



@app.route("/login")
def login():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)


