from django.urls import path

# from friendsystem.views import send_friend_request, accept_friend_request, decline_friend_request
from friendsystem import views
from aroom.views import query_friends_list

app_name = "friendsystem"

urlpatterns = [
    path('friend_request/', views.send_friend_request, name="friend-request"),
    path('accept_friend_request/<friend_request_id>', views.accept_friend_request, name='friend-request-accept'),
    path('decline_friend_request/<friend_request_id>', views.decline_friend_request, name='friend-request-decline'),
    path('cancel_friend_request/<friend_request_id>', views.cancel_friend_request, name='friend-request-cancel'),
    path('unfriend/<user_id>', views.unfriend, name='unfriend'),
]