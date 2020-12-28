from django.urls import path

from .views import AuthorizeUser, signout

urlpatterns = [
    path('', AuthorizeUser.as_view(), name='authorize'),
    path('signout/', signout, name='signout')
]
