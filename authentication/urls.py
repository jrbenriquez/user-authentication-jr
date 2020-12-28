from django.urls import path

from .views import AuthUser, signout

urlpatterns = [
    path('', AuthUser.as_view(), name='authorize'),
    path('signout/', signout, name='signout')
]
