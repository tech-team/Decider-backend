import json
from PIL import Image
import os
import urllib
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
import io
from django.utils import timezone
import requests
from decider_api.log_manager import logger
from decider_api.views.image_views import IMAGE_SIZE
from decider_app.models import Picture
from decider_backend.settings import MEDIA_ROOT


def get_additional_data(user, access_token):
    params = {
        'user_id': user.social_id,
        'fields[]': ['sex', 'city', 'photo_max', 'country'],
        'access_token': access_token,
        'v': 5.43
    }
    data = json.loads(requests.get('https://api.vk.com/method/users.get', params=params).content)['response'][0]

    country = data.get('country')
    city = data.get('city')
    gender = data.get('sex')
    photo_url = data.get('photo_max')

    if country:
        try:
            user_country = get_model('decider_app', 'country').objects.get(name=country.get('title'))
            user.country = user_country
        except ObjectDoesNotExist:
            pass

    if city:
        user.city = city.get('title')
    if gender:
        user.gender = False if gender == 1 else True
    if photo_url:
        fd = urllib.urlopen(photo_url)
        image_file = io.BytesIO(fd.read())

        cur_time = timezone.now().strftime('%s')
        uid = uuid.uuid4().hex
        filename = uid + '.jpg'
        dirname = os.path.join('images', 'avatars', cur_time[:5], cur_time[5:6])
        url = os.path.join(dirname, filename)

        try:
            if not os.path.exists(os.path.join(MEDIA_ROOT, dirname)):
                os.makedirs(os.path.join(MEDIA_ROOT, dirname))

            img = Image.open(image_file)
            resize_scale = max(float(img.size[0])/IMAGE_SIZE[0], float(img.size[1])/IMAGE_SIZE[1])
            if resize_scale > 1:
                img = img.resize((int(img.size[0]/resize_scale), int(img.size[1]/resize_scale)))
            img.save(os.path.join(MEDIA_ROOT, url), 'JPEG', quality=95)

            avatar = Picture.objects.create(url=os.path.join('media', url), uid=uid)

            user.avatar = avatar

        except Exception as e:
            logger.exception(e)

    user.save()
