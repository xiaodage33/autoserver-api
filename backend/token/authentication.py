import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = get_authorization_header(request)  # 获取token
        jwt_value = jwt_value.split()
        if len(jwt_value) != 2:
            raise AuthenticationFailed('认证失败')
        if jwt_value[0].decode() != api_settings.JWT_AUTH_HEADER_PREFIX:
            raise AuthenticationFailed('token头部校验失败')
        jwt_value = jwt_value[1]

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return user, jwt_value
