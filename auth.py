import json
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# My Values
AUTH0_DOMAIN = 'mooves.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://mooves.us/api'
# Token expiration set for 30 days (2592000 sec)

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
    Implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    # Obtains the Access Token from the Authorization Header
    auth = request.headers.get("Authorization", None)
    if not auth:
        abort(401)
        # raise AuthError({"code": "authorization_header_missing",
        #                 "description":
        #                     "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " 'Bearer'"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


'''
Implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not
    in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included'
        }, 400)

    if permission not in payload['permissions']:
        abort(401)
        # raise AuthError({
        #     'code': 'unauthorized',
        #     'description': 'Permissions not found'
        # }, 401)
    return True

# Determines if the required scope is present in the Access Token
# Args: required_scope (str): The scope required to access the resource


def requires_scope(required_scope):
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


'''
Implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):

    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
Implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and
        check the requested permission
    return the decorator which passes the decoded payload to the
        decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            if token is None:
                abort(500)
            try:
                payload = verify_decode_jwt(token)
            except Exception:
                abort(401)
            # _request_ctx_stack.top.current_user = payload
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


#  V2

# https://mooves.us.auth0.com/authorize?audience=https://mooves.us/api&response_type=token&client_id=TQjRW5UYhPXTB7YM1YkZjRhYbtOruOhj&redirect_uri=http://127.0.0.1:5000/callback


# Determines if the Access Token is valid

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if constants.PROFILE_KEY not in session:
#             return redirect('/login')
#         return f(*args, **kwargs)

#     return decorated

# def requires_auth(f):

#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = get_token_auth_header()
#         jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
#         jwks = json.loads(jsonurl.read())
#         unverified_header = jwt.get_unverified_header(token)
#         rsa_key = {}
#         for key in jwks["keys"]:
#             if key["kid"] == unverified_header["kid"]:
#                 rsa_key = {
#                     "kty": key["kty"],
#                     "kid": key["kid"],
#                     "use": key["use"],
#                     "n": key["n"],
#                     "e": key["e"]
#                 }
#         if rsa_key:
#             try:
#                 payload = jwt.decode(
#                     token,
#                     rsa_key,
#                     algorithms=ALGORITHMS,
#                     audience=API_AUDIENCE,
#                     issuer="https://"+AUTH0_DOMAIN+"/"
#                 )
#             except jwt.ExpiredSignatureError:
#                 raise AuthError({"code": "token_expired",
#                                 "description": "token is expired"}, 401)
#             except jwt.JWTClaimsError:
#                 raise AuthError({"code": "invalid_claims",
#                                 "description":
#                                     "incorrect claims,"
#                                     "please check the audience and issuer"},
#                                 401)
#             except Exception:
#                 raise AuthError({"code": "invalid_header",
#                                 "description":
#                                     "Unable to parse authentication"
#                                     " token."}, 401)

#             _request_ctx_stack.top.current_user = payload
#             return f(*args, **kwargs)
#         raise AuthError({"code": "invalid_header",
#                         "description": "Unable to find appropriate key"},
#  401)
#     return decorated
