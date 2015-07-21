from PIL import Image
import httplib
import os
import uuid
from django.utils import timezone
from decider_api.log_manager import logger
from decider_app.views.utils.response_codes import CODE_IMAGE_UPLOAD_FAILED, CODE_BAD_IMAGE
from decider_backend.settings import MEDIA_ROOT


SHARE_SIZE = (1400, 2000)
IMAGE_SIZE = (720, 1280)
PREVIEW_SIZE = (720, 1280)


def upload_image(image, preview=None, upload_to='misc'):

    response = {}

    cur_time = timezone.now().strftime('%s')
    uid = uuid.uuid4().hex
    filename = uid + '.jpg'
    dirname = os.path.join('images', upload_to, cur_time[:5], cur_time[5:6])
    url = os.path.join(dirname, filename)

    try:
        if not os.path.exists(os.path.join(MEDIA_ROOT, dirname)):
            os.makedirs(os.path.join(MEDIA_ROOT, dirname))
    except Exception as e:
        logger.exception(e)
        response['error'] = (httplib.INTERNAL_SERVER_ERROR, CODE_IMAGE_UPLOAD_FAILED, 'Image upload failed')
        return response

    try:
        img = Image.open(image)
        resize_scale = max(float(img.size[0])/IMAGE_SIZE[0], float(img.size[1])/IMAGE_SIZE[1])
        if resize_scale > 1:
            img = img.resize((int(img.size[0]/resize_scale), int(img.size[1]/resize_scale)))
        img.save(os.path.join(MEDIA_ROOT, url), 'JPEG', quality=95)
    except Exception as e:
        logger.exception(e)
        response['error'] = (httplib.BAD_REQUEST, CODE_BAD_IMAGE, 'Bad image')
        return response

    if preview:
        preview_filename = uid + '_preview.jpg'
        preview_url = os.path.join(dirname, preview_filename)

        try:
            preview = Image.open(preview)
            resize_scale = max(float(preview.size[0])/PREVIEW_SIZE[0], float(preview.size[1])/PREVIEW_SIZE[1])
            if resize_scale > 1:
                preview = preview.resize((int(preview.size[0]/resize_scale), int(preview.size[1]/resize_scale)))
            preview.save(os.path.join(MEDIA_ROOT, preview_url), 'JPEG', quality=95)
        except Exception as e:
            logger.exception(e)
            response['error'] = (httplib.BAD_REQUEST, CODE_BAD_IMAGE, 'Bad preview')
            return response

    response['data'] = {
        'image_url': url,
        'preview_url': preview_url if preview else None,
        'uid': uid
    }
    return response