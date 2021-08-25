from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from aroom.models import Contact
from datetime import datetime
from friendsystem.models import FriendList, FriendRequest
from django.conf import settings
from friendsystem.utils import get_friend_request_or_false
from friendsystem.friend_request_status import FriendRequestStatus

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')
def base(request):
    return render(request, 'test.html')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        address = request.POST.get('address')
        contact = Contact(Name=name, Email=email, Address=address, Messages=message, Date=datetime.today())
        contact.save()
        messages.success(request, 'Your massage has been sent!')
    return render(request, 'contactus.html')

def log_in(request):
    if request.method == "POST":
        # check that user login with correct credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def log_out(request):
    print("Nitin")
    logout(request)
    return redirect("/login")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        address = request.POST.get('address')
        image = request.FILES.get('image')
        password = request.POST['password']
        re_password = request.POST['re_password']

        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return render(request, 'signup.html')
        if password != re_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        # creat user
        myuser = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname, image=image, date=datetime.today())
        
        myuser.save()
        messages.success(request, 'Your account has been successfully created Please Login.')
    return render(request, 'signup.html')


def room(request, room_name):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'room.html', {
        'room_name': room_name
    })

def findfriend(request):
    if request.method == "POST" and request.POST.get('find'):
        name = request.POST.get('find')
        query_set = User.objects.filter(first_name__icontains=name)
        print(query_set)
        dic = {"info": query_set}
        return render(request, "findfriend.html", dic)
    return render(request, "findfriend.html")

def profile(request, *args, **kwargs):
    context = {}
    if request.method == "POST":
        user_id = request.POST.get('id')
    else:
        user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("user not found")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['email'] = account.email
        context['address'] = account.address
        context['image'] = account.image.url

        friend_requests = None
        request_sent = FriendRequestStatus.NO_REQUEST_SENT

        try:
            # getting friend list
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        # friends have list of Friends
        friends = friend_list.friends.all()
        context["friends"] = friends
        # Define state template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            # we are viewing another user account which means you are not looking own profile
            is_self = False
            if friends.filter(id=user.id):
                # we are searching own name in another user's friend list if we get our name in that which means that we are frineds if not then we are not friends
                is_friend = True
            else:
                is_friend = False
                # if you are not friend then
                # Case1: Request has been sent from THEM TO YOU
                # FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # Case2: Request has been sent from YOU TO THEM:
                # FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=user, receiver=account).id
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # Case3: No request has been sent.
                # FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        elif not user.is_authenticated:
            is_self = False
        else:
            # it means you are looking your own profile
            # now getting the friend requests which are sent to you from them
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except Exception as e:
                pass
                # return HttpResponse("no friend request")

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        # context['BASE_URL'] = settings.BASE_URL
        return render(request, 'profile.html', context)

def query_friends_list(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get('user_id')
    account = User.objects.get(id=user_id)
    
    if user.is_authenticated:
        if user != account:
            # it means you are not looking at your own friendlist
            friend_list = FriendList.objects.get(user=account)
            if friend_list.is_private:
                # friend list is private
                friends = "Friend list is private"
            else:
                # friend list is not private
                friends = friend_list.friends.all()
        else:
            # now you looking at your own friend list 
            friend_list = FriendList.objects.get(user=account)
            friends = friend_list.friends.all()
    else:
        return redirect("/login")
    context['friends'] = friends
    return render(request, 'friends.html', context)

def query_friend_request(request, *args, **kwargs):
    context = {}
    user = request.user
    account_id = kwargs.get("user_id")
    account = User.objects.get(id=account_id)
    if user.is_authenticated:
        if user == account:
        # it checks that you are looking for your own requests
            requests = FriendRequest.objects.filter(receiver=account, is_active=True)
            context['requests'] = requests
        else:
            return redirect("/")
    else:
        return redirect("/login")
    return render(request, "friend_request.html", context)


def mychat(request, *args, **kwargs):
    context = {}
    account_id = kwargs.get("chat_id")
    user = request.user
    try:
        account = User.objects.get(id=account_id)
    except User.DoesNotExist:
        return HttpResponse("user not found")
    if user.is_authenticated and account:
        if account != user:
            # this means we are not looking for own chat room
            try:
                # getting account's friend list
                account_friend_list = FriendList.objects.get(user=account)
            except FriendList.DoesNotExist:
                friend_list = FriendList(user=account)
                friend_list.save()
            
            account_friends = account_friend_list.friends.all()
            if account_friends.filter(id=user.id):
                #  we are searching own name in another user's friend list if we get our name in that which means that we are frineds if not then we are not friends
                context["chat_id"] = account_id
                return render(request, "mychat.html", context)
            else:
                return redirect("/")
        else:
            # this means we are requested for own chat room 
            context["chat_id"] = account_id 
            return render(request, "mychat.html", context)
    else:
        return HttpResponse("Something went wrong")