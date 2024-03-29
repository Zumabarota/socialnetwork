from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Comment, Dweet, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username", "email"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# admin.site.register(Profile)
admin.site.register(Dweet)
admin.site.register(Comment)
