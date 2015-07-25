from django.shortcuts import render, redirect
from social.exceptions import AuthAlreadyAssociated, AuthCanceled


class SocialAuthMiddleware(object):
    def process_exception(self, request, exception):
        if exception.__class__ == AuthAlreadyAssociated:
            return render(request, 'social_login.html', {'text': 'That account is already in use.'})
        elif exception.__class__ == AuthCanceled:
            response = redirect('api:social_complete')
            response['Location'] += '?canceled=1'
            return response
        else:
            return
