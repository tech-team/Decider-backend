import httplib
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_api.utils import helper
from decider_api.utils.endpoint_decorators import require_registration
from decider_api.utils.helper import get_user_data
from decider_app.models import User
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_UNKNOWN_USER, CODE_INVALID_DATA, CODE_OK, \
    CODE_CREATED, CODE_SERVER_ERROR, CODE_USERNAME_TAKEN, CODE_REGISTRATION_UNFINISHED, CODE_INSUFFICIENT_CREDENTIALS


class UserDataEndpoint(ProtectedResourceView):
    EDITABLE_FIELDS = ['username', 'first_name', 'last_name', 'middle_name',
                       'is_anonymous', 'gender', 'birthday',
                       'about', 'country', 'city', 'avatar']

    def get(self, request, *args, **kwargs):
        try:
            try:
                if not kwargs.get('user_id'):
                    user_id = request.resource_owner.id
                else:
                    user_id = int(kwargs.get('user_id'))
                    if user_id != request.resource_owner.id and not request.resource_owner.registration_finished():
                        return build_error_response(httplib.BAD_REQUEST, CODE_REGISTRATION_UNFINISHED,
                                                    "Registration unfinished")

                if not user_id:
                    raise ValueError('Error: user_id is ' + str(user_id))
            except Exception as e:
                logger.exception(e)
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ['user_id'])

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_USER,
                                            "No user with specified id")

            return build_response(httplib.OK, CODE_OK, "User fetched successfully", get_user_data(user))
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_SERVER_ERROR,
                                        "Failed to fetch user")

    def post(self, request, *args, **kwargs):
        user = request.resource_owner

        username = request.POST.get('username')

        if not username and not user.registration_finished():
            return build_error_response(httplib.BAD_REQUEST, CODE_INSUFFICIENT_CREDENTIALS,
                                        'Username is required to finish registration')

        if username:
            if User.objects.filter(username=username).exclude(uid=user.uid).count() > 0:
                return build_error_response(httplib.BAD_REQUEST, CODE_USERNAME_TAKEN,
                                            "Username taken")
            else:
                user.username = username

        user.save()

        return build_response(httplib.CREATED, CODE_CREATED, "User successfully updated", get_user_data(user))
