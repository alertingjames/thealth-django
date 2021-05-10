from django.conf.urls import url
from . import views

app_name='imageagent'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'login', views.login, name='login'),
    url(r'signup', views.signup, name='signup'),
    url(r'forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'resetpassword', views.resetpassword, name='resetpassword'),
    url(r'rstpwd', views.rstpwd, name='rstpwd'),
    
    
]