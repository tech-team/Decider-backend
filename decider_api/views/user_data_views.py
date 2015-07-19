import httplib
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_api.utils import helper
from decider_api.utils.endpoint_decorators import track_activity
from decider_api.utils.helper import get_user_data
from decider_app.models import User
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_UNKNOWN_USER, CODE_INVALID_DATA, CODE_OK, \
    CODE_CREATED, CODE_SERVER_ERROR


class UserDataEndpoint(ProtectedResourceView):
    @track_activity
    def get(self, request, *args, **kwargs):
        try:
            try:
                if not kwargs.get('user_id'):
                    user_id = request.resource_owner.id
                else:
                    user_id = int(kwargs.get('user_id'))

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


class UserEditEndpoint(ProtectedResourceView):

    EDITABLE_FIELDS = ['first_name', 'last_name', 'middle_name',
                       'is_anonymous', 'gender', 'birthday',
                       'about', 'country', 'city', 'avatar']

    @track_activity
    def post(self, request, *args, **kwargs):
        user = request.resource_owner

        data = request.POST.get('data')

        return build_response(httplib.CREATED, CODE_CREATED, "VASYA", {'email': user.email})
