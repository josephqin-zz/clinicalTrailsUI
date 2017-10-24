from django.conf.urls import url
from landscape import views


urlpatterns = [
    url(r'^$', views.ls, name='landscapeDemo'),

]