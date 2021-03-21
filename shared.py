import os
import jwt
import pandas as pd
from config import Config
basedir = os.path.abspath(os.path.dirname(__file__))

users = [
    {
        'name': 'Ajit Jadhav',
        'email': 'ajit.jadhav@technocrunch.com',
        'department': 'Tech Service'
    }
]

class User:
    def __init__(self, token = None):
        self.token = token
    
    def verify(self):
        if not self.token:
            return False
        else:
            try:
                decoded = jwt.decode(self.token, 'secret', algorithms=['RS256', 'HS256'])
                if decoded:
                    return True
                else:
                    return False
            except Exception as error:
                print(str(error))
                return False
    
    def get_user_data(self):
        try:
            decoded = jwt.decode(self.token, 'secret', algorithms=['RS256', 'HS256'])
            if decoded:
                return decoded
            else:
                return None
        except:
            return None

class Authentication:
    def __init__(self, payload = None):
        self.payload = payload
    
    def generate_token(self):
        try:
            if self.payload:
                df = pd.DataFrame(users)
                if len(list(df[df['email'] == self.payload['email']]['email'].unique())):
                    token = jwt.encode(self.payload, Config.SECRET_KEY)
                    if token:
                        return True, token, None
                    else:
                        return False, None, 'Error while generating the token'
                else:
                    return False, None, 'No user found'
            else:
                return False, None, 'No Payload given'
        except Exception as error:
            return False, None, str(error)