from oauth2_provider.views import ProtectedResourceView
from decider_app.models import User
from decider_app.views.utils.response_builder import build_ok_response, build_404_response



class UserDataEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return build_404_response('No user with that id', http_code=404)

        user = {
            'email': user.email,
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'birthday': user.birthday,
            'country': user.country,
            'city': user.city,
            'about': user.about,
            'gender': user.gender
        }
        return build_ok_response(user)


class UserEditEndpoint(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        owner = request.resource_owner
        return build_ok_response({'email': owner.email})