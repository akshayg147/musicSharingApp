from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/upload/', views.upload_music, name='upload'),
]


