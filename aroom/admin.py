from django.contrib import admin

# Register your models here.
from .models import Contact, User
from django.contrib.auth.admin import UserAdmin

# this is how we register our model with different style
@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('email','id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {
            "fields": (
                'date',
                'email',
                'password',
                'username',
                'first_name',
                'last_name',
                'image',
                'address',
            ),
        }),
        ('permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            "fields": (
                'email',
                'username',
                'image',
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'date'
            ),
        }),
    )
    

    ordering = ('email',)



# this is how we register our model 
admin.site.register(Contact)

