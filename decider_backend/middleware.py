from django.shortcuts import render
from social.exceptions import AuthAlreadyAssociated


class SocialAuthMiddleware(object):
    def process_exception(self, request, exception):
        if exception.__class__ == AuthAlreadyAssociated:
            return render(request, 'social_login.html', {'text': 'That account is already in use.'})
        else:
            return
