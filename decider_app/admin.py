from django.contrib import admin
from models import *

admin.site.register(Country)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Poll)
admin.site.register(PollItem)
admin.site.register(Vote)
