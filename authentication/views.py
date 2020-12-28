import base64

from hashlib import sha256
from urllib.parse import urlencode

from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
# Create your views here.

User = get_user_model()

# Create an authorizing endpoint that :
from rest_framework import serializers


def signout(request):
    logout(request)
    return redirect(settings.FRONTEND_URL)

def hash_string(string):
    encoding = 'utf-8'
    s = sha256()
    s.update(str.encode(string))
    hashed_token = base64.urlsafe_b64encode(s.digest()).decode(encoding)
    return hashed_token


class AuthSerializer(serializers.Serializer):
    redirect = serializers.CharField()


class AuthUser(CreateAPIView):
    serializer_class = AuthSerializer
    authentication_classes = [] # Improve later to limit only to one domain
    permission_classes = []

    def create(self, request, *args, **kwargs):
        # Get the data from POST
        data = request.data
        username = data.get('username')
        password = data.get('password')
        redirect_url = data.get('redirect_url')

        # Check data
        if not username:
            raise NotFound('No Username Found')
        if not password:
            raise NotFound('No Password Found')
        if not redirect_url:
            raise NotFound('No Redirect Url Found')
        try:
            user = User.objects.get(username=username)
        except:
            raise NotFound('User Not Found')

        if not user.check_password(password):
            raise NotFound('Credentials Not Matching')

        if hasattr(user, 'auth_token'):
            token = user.auth_token
            token.delete()

        token = Token.objects.create(user=user)
        hashed_token = hash_string(token.key)

        query_params = {"r": user.id,
                        "auth_token": hashed_token,
                        "redirect_url": redirect_url,
                        }
        query_string = urlencode(query_params)
        cookie_url = reverse('set-cookie')

        clientdata = {
                  "redirect": "{}{}?{}".format(settings.PUBLIC_PATH, cookie_url, query_string)
        }

        serializer = AuthSerializer(data=clientdata)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# generate url for set cookie with hashed token and redirect url as query params


# Create a view that sets the cookie on GET

def set_cookie(request):
    if request.method == 'GET':
        # Get Data
        auth_hashed = request.GET.get('auth_token')
        user_id = request.GET.get('r')
        redirect_url = request.GET.get('redirect_url')

        if any([not auth_hashed, not user_id, not redirect_url]):
            return StreamingHttpResponse('Oops something went wrong please go back and login 1')


        try:
            user = User.objects.get(id=user_id)
        except:
            return StreamingHttpResponse('Oops something went wrong please go back and login')

        if not hasattr(user, 'auth_token'):
            return StreamingHttpResponse('Oops something went wrong please go back and login')

        token = user.auth_token
        checker_hash = hash_string(token.key)

        if checker_hash != auth_hashed:
            return StreamingHttpResponse('Oops something went wrong please go back and login')

        token.delete()

        login(request, user)

        return render(request, "authorize.html", context={"redirect_url": redirect_url})

