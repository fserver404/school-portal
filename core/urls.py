from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="home"),         # صفحه ریشه = لاگین
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("subjects/", views.subjects_view, name="subjects"),
]