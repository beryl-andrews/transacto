from django.urls import path
from . import views

urlpatterns = [
            path("", views.home, name="home"),
            path("login", views.login, name="login"),
            path("register", views.register, name="register"),
            path('logout/', views.logout, name='logout'),
            path("admin-dashboard", views.admin_dashboard, name="admin_dashboard"),
            path("user-dashboard", views.user_dashboard, name="user_dashboard")
        ]
