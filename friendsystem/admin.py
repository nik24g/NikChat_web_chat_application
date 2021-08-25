from django.contrib import admin
from .models import FriendList, FriendRequest
# Register your models here.

@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user', 'user_id', 'pk']
    search_fields = ['user']
    # readonly_fields = ['user']
   

    class Meta:
        model = FriendList

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver','is_active']
    list_display = ['id', 'sender', 'receiver', 'is_active']
    search_fields = ['sender__username','sender__email', 'receiver__username', 'receiver__email','is_active']

    class Meta:
        model = FriendRequest

# admin.site.register(demo)
# admin.site.register(FriendList)