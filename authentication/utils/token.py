import hashlib

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings


# check if user has token
def has_a_token(user):
    try:
        token = Token.objects.get(user=user)
        return True
    except:
        return False


# create token
def create_token(user, use_recent=False):
    token = Token.objects.filter(user=user).order_by('created')
    if use_recent and token:
        reference_date = datetime.now() - timedelta(minutes=5)
        latest_token = token.last()
        if latest_token.created > reference_date:
            return latest_token

    token.delete()
    token = Token.objects.create(user=user)
    return token


# create refresh token
def create_refresh_token(token):
    key = token.key
    refresh_token = hashlib.sha256("{}-app-name".format(key)).hexdigest()
    user = token.user
    user.refresh_token = refresh_token
    user.save()
    return refresh_token


# this return left time
def expires_in(token):
    time_elapsed = datetime.now() - token.created
    left_time = timedelta(seconds=settings.REST_FRAMEWORK_TOKEN_SECONDS_EXPIRY) - time_elapsed
    return left_time


# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# If token is expired then it will be removed

def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = None
    return is_expired, token


# ________________________________________________
# DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """

    def authenticate_credentials(self, key):

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")
        return (token.user, token)
