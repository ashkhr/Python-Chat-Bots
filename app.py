from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User_auth(db.Model):
    
    __tablename__ = 'user_auth'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #primary_key=True
    usernames = db.Column(db.String)
    email= db.Column(db.String)
    category = db.Column(db.String)
    topic = db.Column(db.String)
    areyou = db.Column(db.String)
    tracking_number = db.Column(db.String)
    
    
    def __repr__(self, usernames):
        self.usernames=usernames


if __name__=='__main__':
	db.create_all()