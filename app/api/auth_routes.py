from . import api
from ..models import User
from flask import request

@api.post('/signup')
def signUpAPI():
    # when you are creating an API that expects a POST, you should make a doctype
    """
        WHAT DOES THE EXPECTED REQUEST BODY LOOK LIKE
    """
    # we are just gonna assume they gave us the right info
    data = request.json
            # the same request as if request.method == 'POST'
    
    # this is a lot like getting info from a form
    # username = form.username.data
    
    username = data['username']
    email = data['email']
    password = data['password']

    # THIS IS A LOT LIKE THE signUp From auth/routes.py
    
    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'status' : 'not ok',
            'message' : 'That username is taken. Please choose a different username.'
        }, 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status' : 'not ok',
            'message' : 'That email is already in use. Please choose a different email.'
        }, 400
    
    user = User(username, email, password)
    
    user.save_to_db()

    return {
        'status' : 'ok',
        'message' : 'you have successfully created an account'
    }, 201 # successfully Created something