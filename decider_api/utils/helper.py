

def get_short_user_data(user):
    return {
        "id": user.id,
        'uid': user.uid,
        "username": user.username,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "avatar": user.avatar.url if user.avatar else None
    }


def get_short_user_row_data(row, columns, prefix):
    return {
        'id': row[columns.index(prefix + '_id')],
        'uid': row[columns.index(prefix + '_uid')],
        'username': row[columns.index(prefix + '_username')],
        'first_name': row[columns.index(prefix + '_first_name')],
        'last_name': row[columns.index(prefix + '_last_name')],
        'middle_name': row[columns.index(prefix + '_middle_name')],
        'avatar': row[columns.index(prefix + '_image_url')]
    },