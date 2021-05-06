
from django.urls import path, re_path
from dashboard.views import *
from django.contrib.auth.decorators import login_required
app_name = 'dashboard'

urlpatterns = [
    path(r'',  login_required(dashboardView.as_view()), name='dashboard_page'),
    re_path(r'products-data/$', login_required(productDataView.as_view()), name='products'),
    path(r'data-view/<slug:data_id>/', login_required(productDetailView.as_view()), name='product_detail'),
]