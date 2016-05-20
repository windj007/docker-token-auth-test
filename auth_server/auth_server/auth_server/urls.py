from django.conf.urls import url

from auth_server.views import get_token

urlpatterns = [
    url(r'^token/$', get_token, name = 'token_auth'),
]
