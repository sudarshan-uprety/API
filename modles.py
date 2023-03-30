from mongoengine import *
from passlib.hash import pbkdf2_sha1
import datetime

def db_connection():
    connect(host="mongodb://localhost:27017/mydatabase")

def db_disconnect():
    disconnect()

class User(Document):
    first_name=StringField(max_length=30,required=True)
    last_name=StringField(max_length=30,required=True)
    email=EmailField(required=True,unique=True)
    phone=IntField(required=True,unique=True)
    password = StringField(required=True,password=True)
    confirm_password = StringField(password=True)
    created_at=DateTimeField(default=datetime.datetime.now)
    
    def set_password(self,password):
        self.password=pbkdf2_sha1.hash(password)

    def check_password(self,password):
        return pbkdf2_sha1.verify(password,self.password)

    meta = {
        'collection': 'User',
        'strict': False

    }


class Post(Document):
    user_id = StringField(required=True)
    title=StringField(max_length=100, required=True)
    body=StringField(max_length=1000,required=True)
    created_at=DateTimeField(default=datetime.datetime.now)


    def all(self):
        return Post.objects(user_id=self.user_id)
    meta = {
        'collection': 'Post',
        'strict': False
    }


class Vote(Document):
    post_id=StringField(required=True)
    user_id=StringField(required=True)
    vote=IntField(required=True,default=0,min_value=0,max_value=5)
    voted_date=DateTimeField(default=datetime.datetime.now)


    meta = {
        'collection': 'Vote',
        'strict': False
    }