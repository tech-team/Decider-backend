

def get_short_user_data(user):
    return {
        'uid': user.uid,
        "username": user.username,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "avatar": user.avatar.url if user.avatar else None
    }


def get_short_user_row_data(row, columns, prefix):
    return {
        'uid': row[columns.index(prefix + '_uid')],
        'username': row[columns.index(prefix + '_username')],
        'first_name': row[columns.index(prefix + '_first_name')],
        'last_name': row[columns.index(prefix + '_last_name')],
        'middle_name': row[columns.index(prefix + '_middle_name')],
        'avatar': row[columns.index(prefix + '_image_url')]
    }


def get_user_data(user):
    if user.social_id and user.social_site:
        data = {
            'social_id': user.social_id,
            'social_site': user.social_site.name
        }
    else:
        data = {
            'email': user.email
        }

    data.update({
        'uid': user.uid,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'middle_name': user.middle_name,
        'is_anonymous': user.is_anonymous,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'country': user.country,
        'city': user.city,
        'birthday': user.birthday,
        'gender': user.gender,
        'about': user.about,
        'avatar': user.avatar.url if user.avatar else None
    })

    return data
