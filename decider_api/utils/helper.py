from time import strftime, timezone
import datetime

BACKENDS = {
    'vk': 'vk-oauth2'
}

def str2bool(v):
    if not v:
        return None
    elif v is True:
        return True
    else:
        return v.lower() in ("yes", "true", "t", "1")

def get_short_user_data(user, is_anonymous=False, force_deanon=False):
    if (is_anonymous or user.is_anonymous) and not force_deanon:
        return {
            'uid': 'anonymous',
            "username": 'anonymous',
            "last_name": 'anonymous',
            "first_name": 'anonymous',
            "middle_name": 'anonymous',
            "avatar": None
        }
    else:
        return {
            'uid': user.uid,
            "username": user.username,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "avatar": user.avatar.url if user.avatar else None
        }


def get_short_user_row_data(row, columns, prefix, is_anonymous=False, force_deanon=False):
    if (is_anonymous or row[columns.index(prefix + '_anonymous')]) and not force_deanon:
        return {
            'uid': 'anonymous',
            "username": 'anonymous',
            "last_name": 'anonymous',
            "first_name": 'anonymous',
            "middle_name": 'anonymous',
            "avatar": None
        }
    else:
        return {
            'uid': row[columns.index(prefix + '_uid')],
            'username': row[columns.index(prefix + '_username')],
            'first_name': row[columns.index(prefix + '_first_name')],
            'last_name': row[columns.index(prefix + '_last_name')],
            'middle_name': row[columns.index(prefix + '_middle_name')],
            'avatar': row[columns.index(prefix + '_image_url')]
        }


def get_user_data(user, is_anonymous=False, force_deanon=False):

    if (is_anonymous or user.is_anonymous) and not force_deanon:
        data = {
            'is_anonymous': True,
            'is_active': user.is_active
        }
        for field in ['email', 'uid', 'username', 'first_name', 'last_name', 'middle_name',
                      'about']:
            data[field] = 'anonymous'
        for field in ['date_joined', 'last_login', 'gender', 'country', 'city', 'birthday',
                      'avatar']:
            data[field] = None
        return data

    gender = None
    if user.gender is True:
        gender = 'M'
    elif user.gender is False:
        gender = 'F'

    return {
        'email': user.email,
        'uid': user.uid,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'is_anonymous': user.is_anonymous,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'country': user.country.name if user.country else None,
        'city': user.city,
        'birthday': user.birthday.strftime("%Y-%m-%d") if user.birthday and
                                                          user.birthday >= datetime.date(1900, 1, 1) else None,
        'gender': gender,
        'about': user.about,
        'avatar': user.avatar.url if user.avatar else None
    }


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def check_params_types(params, cast_type=int):
    errors = []
    for param in params:
        if params[param]:
            try:
                cast_type(params[param])
            except ValueError:
                errors.append(param)
    return errors

