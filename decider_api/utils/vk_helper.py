import json
import os
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
import io
import requests
from decider_api.utils.image_helper import upload_image
from decider_app.models import Picture


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

        result = upload_image(image_file, preview=None, upload_to='avatars')
        if not result.get('error'):
            data = result.get('data')
            avatar = Picture.objects.create(url=os.path.join('media', data.get('image_url')),
                                            uid=data.get('uid'))
            user.avatar = avatar

    user.save()
