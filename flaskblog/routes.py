from flask import Flask, render_template, url_for, flash, redirect, request
from flaskblog.models import User
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app, db, bcrypt, socketio
from flask_login import login_user, current_user, logout_user, login_required
from math import radians, cos, sin, asin, sqrt
import geocoder
from flask_socketio import SocketIO

#!-----------------------------------------------------------------------------------------------------

def dist(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
#!-------------------------------------------------------------------------------------------------------
def get_coordinates():
	g = geocoder.ip('me')
	latitude = g.latlng[0]
	longitude = g.latlng[1]
	location = str(str(latitude) + str(longitude))
	return(location)
#!------------------------------------------------------------------
	


def listofusers():
	users = User.query.all()
	
	s = []
	c = []
	c1 = []
	c2 = []
	
	if current_user.is_authenticated:
		for user in users:
			
			if user == current_user:
				continue

			lat1 = float(current_user.gps[0:7])
			lon1 = float(current_user.gps[7:14])
			lat2 = float(user.gps[0:7])
			lon2 = float(user.gps[7:14])
			d = dist(lat1, lon1, lat2, lon2)

			same_school = (current_user.school == user.school)
			same_college = (current_user.college == user.college)
			same_company1 = (current_user.company1 == user.company1)
			same_company2 = (current_user.company2 == user.company2)

			if(d<20 and same_school):
				s.append(user)
			
			if(d<20 and same_college and not(same_school)):
				c.append(user)
			
			if(d<20 and same_company1 and not(same_school or same_college)):
				c1.append(user)
			
			if(d<20 and same_company2 and not(same_school or same_college or same_company2) ):
				c2.append(user)

	return(s,c,c1,c2)
#!------------------------------------------------------------------------------------------------
def net_list():
	s,c,c1,c2 = listofusers()
	return(s+c+c1+c2)
#!------------------------------------------------------------------------------------------------

@app.route("/")
@app.route("/home")
def home():
	s,c,c1,c2 = listofusers()
	total = net_list()
	return render_template('home.html', title= 'Home', s=s, c=c, c1=c1, c2=c2, total=total, lat=float(get_coordinates()[0:7]), lon=float(get_coordinates()[7:]))
#!------------------------------------------------------------------------------------------------

@app.route("/about")
def about():
	return render_template('about.html')
#!------------------------------------------------------------------------------------------------

@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, school = form.school.data, college = form.college.data, company1 = form.company1.data, company2 = form.company2.data, gps = get_coordinates(), password= hashed_password)
		
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
			current_user.gps = location	
			db.session.commit()
			flash('Login successful','success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful','danger')
			
	return render_template('login.html', title='Login', form=form)
		

		


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account", methods=['GET','POST'])
@login_required 
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.school = form.school.data
		current_user.college = form.college.data
		current_user.company1 = form.company1.data
		current_user.company2 = form.company2.data
		db.session.commit()
		flash('Account Details Updated!','success')
		return redirect(url_for('account'))

	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.school.data = current_user.school
		form.college.data = current_user.college
		form.company1.data = current_user.company1
		form.company2.data = current_user.company2

	return render_template('account.html', title='Account', form=form, lat=float(get_coordinates()[0:7]), lon=float(get_coordinates()[7:]))

@app.route('/chat')
def chat():
    return render_template('chat.html', user=current_user)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!')



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)