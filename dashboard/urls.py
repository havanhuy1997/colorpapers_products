
from django.urls import path, re_path
from dashboard.views import *
from django.contrib.auth.decorators import login_required
app_name = 'dashboard'

urlpatterns = [
    path(r'',  login_required(dashboardView.as_view()), name='dashboard_page'),
    # re_path(r'opportunities/$', OpportunityView.as_view(), name='opportunities'),
]