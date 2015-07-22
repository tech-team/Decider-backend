from django.db import connection
from django.utils import timezone
from decider_app.views.utils.response_codes import I_CODE_ALREADY_VOTED, I_CODE_UNKNOWN_ENTITY, \
    I_CODE_VOTE_OK


GET_QUERY = """ SELECT d_{0}.id as {0}_id, d_{0}_likes.id as like_id
                FROM d_{0}
                  LEFT JOIN d_{0}_likes
                    ON d_{0}.id = d_{0}_likes.{0}_id AND d_{0}_likes.user_id = {1}
                WHERE d_{0}.id = {2};"""


INSERT_COMMENT_QUERY = """INSERT INTO d_comment_likes (user_id, comment_id, creation_date)
                          VALUES ({0}, {1}, {2})"""
INSERT_QUESTION_QUERY = """INSERT INTO d_question_likes (user_id, question_id)
                           VALUES ({0}, {1})"""

DELETE_QUERY = """DELETE FROM d_{0}_likes
                  WHERE user_id={1} AND {0}_id={2}"""

ENTITY_UPDATE_QUERY = """UPDATE d_{0}
                         SET likes_count = likes_count {2} 1
                         WHERE id = {1}"""

LIKES_QUERY = """SELECT likes_count
                 FROM d_{0}
                 WHERE id = {1}"""


def get_vote(entity, entity_id, user_id):
    cursor = connection.cursor()

    cursor.execute(GET_QUERY.format(entity, user_id, entity_id))
    res = cursor.fetchone()

    if res is None:
        cursor.close()
        return I_CODE_UNKNOWN_ENTITY, None
    elif res[1] is not None:
        cursor.execute(LIKES_QUERY.format(entity, entity_id))
        res = cursor.fetchone()
        return I_CODE_ALREADY_VOTED, res
    else:
        cursor.close()
        return I_CODE_VOTE_OK, None


def insert_vote(entity, entity_id, user_id):
    cursor = connection.cursor()

    if entity == 'question':
        cursor.execute(INSERT_QUESTION_QUERY.format(entity, user_id, entity_id))
    else:
        cursor.execute(INSERT_COMMENT_QUERY.format(entity, user_id, entity_id, timezone.now()))
    cursor.execute(ENTITY_UPDATE_QUERY.format(entity, entity_id, "+"))
    cursor.execute(LIKES_QUERY.format(entity, entity_id))
    res = cursor.fetchone()
    cursor.close()

    return res


def delete_vote(entity, entity_id, user_id):
    cursor = connection.cursor()

    cursor.execute(DELETE_QUERY.format(entity, user_id, entity_id))
    cursor.execute(ENTITY_UPDATE_QUERY.format(entity, entity_id, "-"))
    cursor.execute(LIKES_QUERY.format(entity, entity_id))
    res = cursor.fetchone()
    cursor.close()

    return res