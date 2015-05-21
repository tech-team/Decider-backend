from django.db import connection

QUERY = """ SELECT d_poll_item.id, d_poll_item.question_id, d_poll_item.text,
                   d_picture.url as image_url, d_picture.preview_url as preview_url,
                   d_poll_item.votes_count, d_vote.id as voted
            FROM d_poll_item
              LEFT JOIN d_picture ON d_poll_item.picture_id = d_picture.id
              LEFT JOIN d_vote ON d_vote.user_id = {}
                              AND d_vote.poll_item_id = d_poll_item.id
        """

WHERE = """ WHERE d_poll_item.poll_id in (%s)"""


def get_poll_items(user_id, poll_ids=None):
    cursor = connection.cursor()

    query = QUERY.format(user_id)
    if poll_ids:
        poll_ids = (', '.join([str(x) for x in poll_ids]))
        cursor.execute((query + WHERE) % poll_ids)
    else:
        cursor.execute(query)

    poll_items = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return poll_items, columns