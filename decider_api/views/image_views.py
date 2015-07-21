import httplib
import os
from django.db import transaction
from oauth2_provider.views import ProtectedResourceView
from decider_api.utils.endpoint_decorators import require_registration, track_activity
from decider_api.utils.image_helper import upload_image
from decider_app.models import Picture
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_CREATED, \
    CODE_REQUIRED_PARAMS_MISSING


class ImagesEndpoint(ProtectedResourceView):

    @transaction.atomic
    @track_activity
    @require_registration
    def post(self, request, *args, **kwargs):

        image = request.FILES.get('image')
        preview = request.FILES.get('preview')

        errors = []
        if not image:
            errors.append('image')
        if not preview:
            errors.append('preview')

        if errors:
            return build_error_response(httplib.BAD_REQUEST, CODE_REQUIRED_PARAMS_MISSING,
                                        "Required params are missing", errors)

        result = upload_image(image, preview)
        error = result.get('error')
        if error:
            return build_error_response(*error)
        data = result.get('data')

        Picture.objects.create(url=os.path.join('media', data['image_url']),
                               preview_url=os.path.join('media', data['preview_url']),
                               uid=data['uid'])

        return build_response(httplib.CREATED, CODE_CREATED, "Images uploaded",
                              data={'uid': data['uid']})
