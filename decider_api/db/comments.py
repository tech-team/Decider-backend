from django.db import connection

QUERY = """ SELECT DISTINCT d_comment.id, d_comment.text, d_comment.creation_date, d_comment.likes_count,
                author_user.first_name as author_first_name, author_user.last_name as author_last_name,
                author_user.middle_name as author_middle_name, author_user.username as author_username,
                author_picture.url as author_image_url, author_user.id as author_id
            FROM d_comment
            LEFT JOIN d_user as author_user ON d_comment.author_id = author_user.id
            LEFT JOIN d_picture as author_picture ON author_picture.id = author_user.avatar_id
            WHERE d_comment.question_id in (%s)"""


def get_comments(q_ids):
    cursor = connection.cursor()

    q_ids = (', '.join([str(x) for x in q_ids]))
    cursor.execute(QUERY % q_ids)
    c_list = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return c_list, columns