from django.db import connection

QUERY = """ SELECT d_locale_category.category_id as id, d_locale_category.name as name
            FROM d_locale_category"""


def get_categories(locale_id):
    cursor = connection.cursor()

    where = " WHERE locale_id = %s" % locale_id
    query = QUERY + where
    cursor.execute(query)
    c_list = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return c_list, columns