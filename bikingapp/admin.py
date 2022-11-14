from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, FriendMgmt, Account
from django.contrib.auth.models import User
from .models import Event, FriendMgmt, Workout, Comment

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
admin.site.register(Workout)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "post", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("name", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
