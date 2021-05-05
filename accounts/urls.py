from django.urls import path, re_path
from accounts import views
app_name = 'accounts'

urlpatterns = [

    re_path(r'logout/$', views.logout_data, name='logout_data'),
    re_path(r'login/$', views.login, name='login'),
]