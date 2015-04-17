from django.db import connection
from decider_app.views.utils.response_codes import I_CODE_ALREADY_VOTED, I_CODE_UNKNOWN_ENTITY, \
    I_CODE_VOTE_OK


GET_QUERY = """ SELECT d_{0}.id as {0}_id, d_{0}_likes.id as like_id
                FROM d_{0}
                  LEFT JOIN d_{0}_likes
                    ON d_{0}.id = d_{0}_likes.{0}_id AND d_{0}_likes.user_id = {1}
                WHERE d_{0}.id = {2};"""


INSERT_QUERY = """INSERT INTO d_{0}_likes (user_id, {0}_id)
                  VALUES ({1}, {2})"""


ENTITY_UPDATE_QUERY = """UPDATE d_{0}
                         SET likes_count = likes_count + 1
                         WHERE id = {1}"""


def get_vote(entity, entity_id, user_id):
    cursor = connection.cursor()

    cursor.execute(GET_QUERY.format(entity, user_id, entity_id))
    res = cursor.fetchone()
    cursor.close()
    if res is None:
        return I_CODE_UNKNOWN_ENTITY
    elif res[1] is not None:
        return I_CODE_ALREADY_VOTED
    else:
        return I_CODE_VOTE_OK


def insert_vote(entity, entity_id, user_id):
    cursor = connection.cursor()

    cursor.execute(INSERT_QUERY.format(entity, user_id, entity_id))
    cursor.execute(ENTITY_UPDATE_QUERY.format(entity, entity_id))

    cursor.close()

    return