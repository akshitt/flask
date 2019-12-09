from flaskblog import db, login_manager
from flask_login import UserMixin
#!--------------------------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


#!------------------------------------------------------------------
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)  #primary key implies unique
	# name = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	school = db.Column(db.String(50), nullable=False)
	college = db.Column(db.String(50) )
	company1 = db.Column(db.String(50) )
	company2 = db.Column(db.String(50))
	gps = db.Column(db.String(50))
	password = db.Column(db.String(50), nullable=False)
	

	def __repr__(self):
		return f"User('{self.username}','{self.email}')"
#!------------------------------------------------------------------

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)  
	title = db.Column(db.String(50), nullable=False)
	content = db.Column(db.String(50), nullable=False) 	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
