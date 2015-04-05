from django.db import connection

QUERY = """ SELECT d_poll_item.id, d_poll_item.question_id, d_poll_item.text,
                   d_picture.url as image_url, d_poll_item.votes_count
            FROM d_poll_item
              LEFT JOIN d_picture ON d_poll_item.picture_id = d_picture.id
            WHERE d_poll_item.poll_id in (%s)"""


def get_poll_items(poll_ids):
    cursor = connection.cursor()

    poll_ids = (', '.join([str(x) for x in poll_ids]))
    cursor.execute(QUERY % poll_ids)
    poll_items = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return poll_items, columns