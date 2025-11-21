from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = 'super secret secrets'

def encode_token(user_id, role="mechanic"):
   
    payload = {
        "sub": str(user_id),  # subject must always be a string
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }


    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f): 
    @wraps(f)
    def decoration(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            
            token = request.headers['Authorization'].split()[1]
        
        if not token:
            return jsonify({"error": "token missing from authorization headers"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print(data)
            request.logged_in_user_id = data['sub'] 
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message':'token is expired'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'message':'invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decoration