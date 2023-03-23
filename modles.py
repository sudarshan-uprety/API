from mongoengine import *
from passlib.hash import pbkdf2_sha1

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
    

    # def validate(self,clean=True):
    #     if self.password != self.confirm_password:
    #         raise ValidationError("Password and confirm password fields do not match.")
    
    def set_password(self,password):
        self.password=pbkdf2_sha1.hash(password)

    def check_password(self,password):
        return pbkdf2_sha1.verify(password,self.password)

    meta = {
        'collection': 'User',
        'strict': False

    }
disconnect()
