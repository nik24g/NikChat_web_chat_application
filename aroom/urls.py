from django.urls import path
from . import views

app_name = "aroom"
urlpatterns = [
    path('', views.index, name="home"),
    path('login', views.log_in, name="login"),
    path('signout', views.log_out, name="signout"),
    path('signup', views.signup, name="signup"),
    path('contactus', views.contactus, name="contactus"),
    path('test', views.base, name="base"),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('Mychat/<str:chat_id>/', views.mychat, name='mychat'),
    path('findfriend', views.findfriend, name='findfriend'),
    path('friends/<int:user_id>/', views.query_friends_list, name='friends'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('request/<int:user_id>/', views.query_friend_request, name='request'),
]
