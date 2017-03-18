from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'.*auth_return', views.auth_return, name='auth_return'),
    url(r'.*auth', views.auth, name='auth'),
    url(r'^$', views.auth, name='auth'),
]