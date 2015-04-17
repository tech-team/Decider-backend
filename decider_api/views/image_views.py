from PIL import Image
import httplib
import uuid
import os
from django.db import transaction
from django.utils import timezone
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_app.models import Picture
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_IMAGE_UPLOAD_FAILED, CODE_BAD_IMAGE, CODE_CREATED
from decider_backend.settings import MEDIA_ROOT, IMAGE_SIZE


class ImagesEndpoint(ProtectedResourceView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        cur_time = timezone.now().strftime('%s')
        uid = uuid.uuid4().hex
        filename = uid + '.jpg'
        dirname = MEDIA_ROOT + 'images/' + cur_time[:5] + '/' + cur_time[5:6] + '/'
        url = dirname + filename

        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_IMAGE_UPLOAD_FAILED,
                                        "Image upload failed")

        try:
            Image.open(request.FILES['image']).resize(IMAGE_SIZE).save(url, 'JPEG', quality=95)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.BAD_REQUEST, CODE_BAD_IMAGE,
                                        "Bad image")

        Picture.objects.create(url=url, uid=uid)

        return build_response(httplib.CREATED, CODE_CREATED, "Image uploaded",
                              data={'uid': uid})