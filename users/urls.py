from django.urls import path
from django.contrib.auth.urls import *
from users.views import sign_up_view

urlpatterns = [
    path('signup', sign_up_view, name='sign_up'),

]
