from django.db import connection

SELECT_QUERY = """ SELECT d_comment.id, d_comment.text, d_comment.creation_date, d_comment.likes_count,
                          d_comment.is_anonymous, d_comment.question_id,
                          author_user.first_name as author_first_name, author_user.last_name as author_last_name,
                          author_user.middle_name as author_middle_name, author_user.username as author_username,
                          author_picture.url as author_image_url, author_user.id as author_id,
                          author_user.uid as author_uid, author_user.is_anonymous as author_anonymous,
                          d_comment_likes.id as voted
                   FROM d_comment
                   LEFT JOIN d_user as author_user ON d_comment.author_id = author_user.id
                   LEFT JOIN d_picture as author_picture ON author_picture.id = author_user.avatar_id
                   LEFT JOIN d_comment_likes ON d_comment_likes.user_id = {0}
                         AND d_comment_likes.comment_id = d_comment.id
                   WHERE d_comment.question_id = {1} AND d_comment.is_active=TRUE"""


def get_comments(user_id, q_id, order=None, limit=None, offset=None):
    cursor = connection.cursor()

    query = SELECT_QUERY.format(user_id, q_id)

    if order:
        query += " ORDER BY {0}".format(order)
    if limit:
        query += " LIMIT {0}".format(limit)
    if offset:
        query += " OFFSET {0}".format(offset)

    cursor.execute(query)
    c_list = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return c_list, columns