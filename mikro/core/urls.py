from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('painel/login/', views.NovaInfoLoginView.as_view(), name='login'),
    path('painel/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('painel/', views.dashboard, name='dashboard'),
    path('painel/clientes/', views.clients, name='clients'),
    path('painel/planos-internet/', views.internet_plans, name='plans'),
    path('painel/publicidade/', views.advertising, name='advertising'),
    path('painel/mikrotik/', views.mikrotik, name='mikrotik'),
]
