from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('download/<int:trip_id>/', views.download_plan),
    path('', views.home),
]