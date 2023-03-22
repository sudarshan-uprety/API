# from mongoengine import *
# connect('mydatabase', host='localhost', port=27017)

# # disconnect()

# class User(Document):
#     email=EmailField(required=True,unique=True)
#     first_name=StringField(max_length=30,required=True)
#     last_name=StringField(max_length=30,required=True)
#     password = StringField(required=True,password=True)

#     meta = {
#         'db': 'mydatabase',
#         'collection': 'User',
#         'strict': False

#     }