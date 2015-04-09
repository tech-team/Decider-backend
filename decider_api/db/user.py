from django.db import connection

QUERY = """SELECT d_user.id, d_user.uid, d_user.email, d_user.username,
                  d_user.first_name, d_user.last_name, d_user.middle_name,
                  d_user.is_active, d_user.date_joined, d_user.birthday,
                  d_user.city, d_user.about, d_user.gender,
                  d_country.name as country, d_picture.url as avatar
           FROM d_user
              LEFT JOIN d_country ON d_user.country_id = d_country.id
              LEFT JOIN d_picture ON d_user.avatar_id = d_picture.id"""


def get_user_data(user_id):
    cursor = connection.cursor()

    where = " WHERE d_user.id = %s" % user_id
    query = QUERY + where
    cursor.execute(query)
    user = cursor.fetchone()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return user, columns
