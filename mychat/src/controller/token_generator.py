from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from mychat.src.core.constants import SECRET_KEY
from jose import jwt


class TokenGenrator:
    oath2_bearer = OAuth2PasswordBearer(tokenUrl='token')

    def create_token(self, email: str, user_id: str):
        dic = {'sub': email, 'id': user_id}
        return jwt.encode(dic, SECRET_KEY, algorithm="HS256")

    def current_user(self, token: str = Depends(oath2_bearer)):
        try:
            decod = jwt.decode(token, SECRET_KEY, access_token=['HS256'])
            username: str = decod.get('sub')
            user_id: str = decod.get('id')
            if username is None or user_id is None:
                return {'detail': 'user not found'}
            return {'username': username, 'user_id': user_id}
        except:
            return {'detail': 'user not found'}
