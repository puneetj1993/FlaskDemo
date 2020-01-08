from flask_package import db,login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    image_file = db.Column(db.String(50),nullable=False,default='default.jpg')
    #about_me = db.Column(db.String(140),nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User({},{})>".format(self.username,self.email)

class Blog(db.Model):
    post = db.Column(db.String(80))
    id = db.Column(db.Integer,primary_key=True)
    usernamep = db.Column(db.String(80))
 
    

    def __repr__(self):
        return "<User {} Posts are ({})>".format(self.usernamep,self.post)
