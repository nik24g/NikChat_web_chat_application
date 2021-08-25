from django.db import models
from django.conf import settings

# Create your models here.
class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="User")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friend")
    is_private = models.BooleanField(blank=True, null=False, default=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        # Add new friend
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        # Remove a friend
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        # initiate the action of the unfriend someone
        remover_friends_list = self # the person who is terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        # Is mutual friend?
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """A friend request consist of two main parts:
    1.  SENDER: Person sending/initiating the friend request
    2.  RECEIVER: Person receiving the friend request"""

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """ Accept a friend request
            update both SENDER and RECEIVER friend lists"""
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request.
        It is "declined" by setting the 'is_active' field to False
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request
        It is "declined" by setting the 'is_active' field to False
        This is only different with respect to declining through the notification that is generated
        """
        self.is_active = False
        self.save()