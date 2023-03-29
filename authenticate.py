import jwt

def is_authenticated(self):
        # Extract the Authorization header
    auth_header = self.headers.get('Authorization')
    if auth_header:
            # Extract the token from the header
        token = auth_header
            # Verify the token and return True if it is valid
        return verify_token(token)
    return False


def verify_token(token):
    try:
        # Verify the token using a secret key
        jwt.decode(token, 'mysecret', algorithms=['HS256'])
        return True
    except:
        return False
    

