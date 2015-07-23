# coding=utf-8
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms import CharField
from models import *

class UserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(UserAdminForm, self).is_valid()
        if self.errors.get('email'):
            del self.errors['email']
        return False if self.errors else True

    def clean(self):
        cleaned_data = super(UserAdminForm, self).clean()
        if self.errors.get('email'):
            del self.errors['email']
        cleaned_data['email'] = self.data['email']
        return cleaned_data


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
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
