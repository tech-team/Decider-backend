import httplib
from oauth2_provider.views import ProtectedResourceView
from decider_api.db.user import get_user_data
from decider_api.log_manager import logger
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_UNKNOWN_USER, CODE_INVALID_DATA, CODE_OK, \
    CODE_CREATED, CODE_SERVER_ERROR


class UserDataEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                user_id = int(kwargs.get('user_id'))
                if not user_id:
                    raise ValueError('Error: user_id is ' + str(user_id))
            except Exception as e:
                logger.exception(e)
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ['user_id'])

            user_row, columns = get_user_data(user_id)

            if not user_row:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_USER,
                                            "No user with specified id")

            user = {
                'id': user_row[columns.index('id')],
                'uid': user_row[columns.index('uid')],
                'email': user_row[columns.index('email')],
                'username': user_row[columns.index('username')],
                'last_name': user_row[columns.index('last_name')],
                'first_name': user_row[columns.index('first_name')],
                'middle_name': user_row[columns.index('middle_name')],
                'is_active': user_row[columns.index('is_active')],
                'date_joined': user_row[columns.index('date_joined')],
                'birthday': user_row[columns.index('birthday')],
                'country': user_row[columns.index('country')],
                'city': user_row[columns.index('city')],
                'about': user_row[columns.index('about')],
                'gender': user_row[columns.index('gender')],
                'avatar': user_row[columns.index('avatar')]
            }

            return build_response(httplib.OK, CODE_OK, "User fetched successfully", user)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_SERVER_ERROR,
                                        "Failed to fetch user")


class UserEditEndpoint(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        owner = request.resource_owner
        return build_response(httplib.CREATED, CODE_CREATED, "VASYA", {'email': owner.email})