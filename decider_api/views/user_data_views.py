import httplib
import os
import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import track_activity
from decider_api.utils.helper import get_user_data, str2bool
from decider_api.utils.image_helper import upload_image
from decider_app.models import User, Picture
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_UNKNOWN_USER, CODE_INVALID_DATA, CODE_OK, \
    CODE_CREATED, CODE_SERVER_ERROR, CODE_USERNAME_TAKEN, CODE_REGISTRATION_UNFINISHED, CODE_INSUFFICIENT_CREDENTIALS


class UserDataEndpoint(ProtectedResourceView):

    @track_activity
    def get(self, request, *args, **kwargs):
        try:
            try:
                if not kwargs.get('user_id'):
                    user_id = request.resource_owner.uid
                else:
                    user_id = int(kwargs.get('user_id'))
                    if user_id != request.resource_owner.uid and not request.resource_owner.registration_finished():
                        return build_error_response(httplib.BAD_REQUEST, CODE_REGISTRATION_UNFINISHED,
                                                    "Registration unfinished")

                if not user_id:
                    raise ValueError('Error: user_id is ' + str(user_id))
            except Exception as e:
                logger.exception(e)
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ['user_id'])

            try:
                user = User.objects.get(uid=user_id)
            except User.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_USER,
                                            "No user with specified id")

            return build_response(httplib.OK, CODE_OK, "User fetched successfully", get_user_data(user))
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_SERVER_ERROR,
                                        "Failed to fetch user")

    @track_activity
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
                user.username = username[:20]

        for field in ['first_name', 'last_name', 'city', 'about']:
            value = request.POST.get(field)
            if value is not None:
                try:
                    setattr(user, field, value)
                except Exception as e:
                    logger.exception(e)
                    continue

        country = request.POST.get('country')
        if country is not None:
            try:
                db_country = get_model('decider_app', 'country').objects.get(name=country)
                user.country = db_country
            except ObjectDoesNotExist:
                user.country = None
                pass

        birthday = request.POST.get('birthday')
        if birthday is not None:
            try:
                db_bday = dateutil.parser.parse(birthday).date()
                user.birthday = db_bday
            except (ValueError, TypeError):
                user.birthday = None
                pass

        gender = request.POST.get('gender')
        if gender is not None:
            if gender == 'M':
                user.gender = True
            elif gender == 'F':
                user.gender = False
            else:
                user.gender = None

        avatar = request.FILES.get('avatar')
        if avatar:
            result = upload_image(avatar, upload_to='avatars')
            error = result.get('error')
            if error:
                return build_error_response(*error, errors=['avatar'])

            data = result.get('data')

            picture = Picture.objects.create(url=os.path.join('media', data.get('image_url')),
                                             uid=data.get('uid'),)
            user.avatar = picture

        is_anonymous = str2bool(request.POST.get('is_anonymous'))
        if is_anonymous is not None:
            user.is_anonymous = is_anonymous

        user.save()

        return build_response(httplib.CREATED, CODE_CREATED, "User successfully updated", get_user_data(user, force_deanon=True))
