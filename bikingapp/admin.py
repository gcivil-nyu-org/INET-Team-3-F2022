from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, FriendMgmt, Workout, Comment, CustomUser
# from .models import Account
from django.contrib.auth.models import User

admin.site.register(Event)
admin.site.register(FriendMgmt)
admin.site.register(Workout)
admin.site.register(CustomUser)
# admin.site.register(Snippet)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "body", "post", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("name", "body")
    actions = ["approve_comments"]
    
    def approve_comments(self, request, queryset):
        queryset.update(active=True)
