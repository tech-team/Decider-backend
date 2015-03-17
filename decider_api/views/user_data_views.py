import json
from django.http import HttpResponse, JsonResponse
from oauth2_provider.views import ProtectedResourceView
from decider_app.views.utils.response_builder import build_ok_response


class UserDataEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        user = {
            'email': request.resource_owner.email,
            'username': request.resource_owner.username,
            'last_name': request.resource_owner.last_name,
            'first_name': request.resource_owner.first_name,
            'middle_name': request.resource_owner.middle_name,
        }
        return build_ok_response(user)