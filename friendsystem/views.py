from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
import json

from aroom.models import User
from friendsystem.models import FriendRequest, FriendList
# Create your views here.
 
def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm that is the correct request
            if friend_request.receiver == user:
                # found friend request. Now accept it 
                friend_request.accept()
                payload['response'] = "Friend request accepted"
            else:
                payload['response'] = "You can not accept another account request"
        else:
            payload['response'] = "Unable to accept that request"
    else:
        payload['response'] = "You must be authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def unfriend(request, *args, **kwargs):
    user = request.user
    payload = {}
    user_friend_list = FriendList.objects.get(user_id=user.id)
    if request.method == "GET" and user.is_authenticated:
        
        account_id = kwargs.get("user_id")
        account = User.objects.get(id=account_id)

        if account != user:

            # this will check that you are not trying to unfriend yourself
            
            account_friend_list = FriendList.objects.get(user_id=account_id)
            
            account_friends = account_friend_list.friends.all()
            
            if account_friends.filter(id=user.id):
                user_friend_list.unfriend(account)
                payload['response'] = "Unfriended"
            else:
                payload['response'] = "You are not their friend or you are not in their friends list"
        else:
            payload['response'] = "You can not unfriend yourself"
    else:
        payload['response'] = "You must be authenticated or something went wrong"
    return HttpResponse(json.dumps(payload), content_type="application/json")

def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm that is the correct request
            if friend_request.receiver == user:
                # found friend request. Now decline it 
                friend_request.decline()
                payload['response'] = "Friend request declined"
            else:
                payload['response'] = "You can not decline another's account request"
        else:
            payload['response'] = "Unable to decline that request"
    else:
        payload['response'] = "You must be authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm that is the correct request
            if friend_request.sender == user:
                # found friend request. Now cancel it
                friend_request.cancel()
                payload['response'] = "Friend request cancelled"
            else:
                payload['response'] = "You can not cancel another's account request"
        else:
            payload['response'] = "Unable to decline that request"
    else:
        payload['response'] = "You must be authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")
            

def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(id=user_id)
            try:
                # Get any friend request (active or non active)
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                # find any of them are active
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request")
                        # if none are active then create a new friend request
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Friend request sent"
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                # there are no friend request so create one
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Friend request sent"
            if payload['response'] == None:
                payload['response'] = "Something went wrong"
        else:
            payload['response'] = "Unable to send friend request"
    else:
        payload['response'] = "You must be authenticated to send friend request"
    return HttpResponse(json.dumps(payload), content_type="application/json")
