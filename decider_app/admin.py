# coding=utf-8
from django.contrib import admin
from models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'last_name', 'first_name', 'get_uid']

    def get_username(self, obj):
        if obj.username:
            return obj.username
        else:
            return '------'

    def get_uid(self, obj):
        return obj.uid

    get_uid.short_description = 'uid'
    get_username.short_description = 'username'

admin.site.register(Country)
admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Poll)
admin.site.register(PollItem)
admin.site.register(Vote)
admin.site.register(Category)
admin.site.register(SocialSite)
admin.site.register(Locale)
admin.site.register(LocaleCategory)
admin.site.register(Picture)
