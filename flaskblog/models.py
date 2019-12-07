from flaskblog import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)  #primary key implies unique
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	school = db.Column(db.String(50), nullable=False)
	college = db.Column(db.String(50) )
	company1 = db.Column(db.String(50) )
	company2 = db.Column(db.String(50))
	gps = db.Column(db.String(50))
	img = db.Column(db.String(50), nullable=False, default='default.png')
	password = db.Column(db.String(50), nullable=False)
	

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.img}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)  
	title = db.Column(db.String(50), nullable=False)
	content = db.Column(db.String(50), nullable=False) 	
	img = db.Column(db.String(50), nullable=False, default='default.png')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
