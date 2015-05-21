from PIL import Image
import httplib
from math import floor
import uuid
import os
from django.db import transaction
from django.utils import timezone
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import require_params
from decider_app.models import Picture
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_IMAGE_UPLOAD_FAILED, CODE_BAD_IMAGE, CODE_CREATED, \
    CODE_REQUIRED_PARAMS_MISSING
from decider_backend.settings import MEDIA_ROOT

IMAGE_SIZE = (1280, 720)
PREVIEW_SIZE = (1280, 720)

class ImagesEndpoint(ProtectedResourceView):

    @transaction.atomic
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

        cur_time = timezone.now().strftime('%s')
        uid = uuid.uuid4().hex
        filename = uid + '.jpg'
        preview_filename = uid + '_preview.jpg'
        dirname = os.path.join('images', cur_time[:5], cur_time[5:6])
        url = os.path.join(dirname, filename)
        preview_url = os.path.join(dirname, preview_filename)

        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_IMAGE_UPLOAD_FAILED,
                                        "Image upload failed")

        try:
            img = Image.open(image)
            resize_scale = max(float(img.size[0])/IMAGE_SIZE[0], float(img.size[1])/IMAGE_SIZE[1])
            if resize_scale > 1:
                img = img.resize((int(img.size[0]/resize_scale), int(img.size[1]/resize_scale)))
            img.save(os.path.join(MEDIA_ROOT, url), 'JPEG', quality=95)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.BAD_REQUEST, CODE_BAD_IMAGE,
                                        "Bad image")

        try:
            preview = Image.open(preview)
            resize_scale = max(float(preview.size[0])/PREVIEW_SIZE[0], float(preview.size[1])/PREVIEW_SIZE[1])
            if resize_scale > 1:
                preview = preview.resize((int(preview.size[0]/resize_scale), int(preview.size[1]/resize_scale)))
            preview.save(os.path.join(MEDIA_ROOT, preview_url), 'JPEG', quality=95)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.BAD_REQUEST, CODE_BAD_IMAGE,
                                        "Bad preview")

        Picture.objects.create(url=url, uid=uid, preview_url=preview_url)

        return build_response(httplib.CREATED, CODE_CREATED, "Images uploaded",
                              data={'uid': uid})
