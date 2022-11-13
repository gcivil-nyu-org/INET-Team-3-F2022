from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, FriendMgmt, Account
from django.contrib.auth.models import User

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural: 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline,)

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Event)
admin.site.register(FriendMgmt)
admin.site.register(Account)