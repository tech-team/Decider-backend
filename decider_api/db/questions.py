from django.db import connection


def tab_switch(case):
    return {
        "new": get_new_questions,
        "popular": get_popular_questions,
        "my": get_my_questions
    }.get(case, None)


QUERY = """SELECT DISTINCT d_question.id, d_question.text, d_question.creation_date,
                  d_question.category_id, d_poll.id as poll_id, d_question.author_id,
                  d_question.likes_count, d_question.comments_count, d_question.is_anonymous,
                  d_user.first_name, d_user.last_name, d_user.middle_name,
                  d_user.username, d_picture.url as image_url
           FROM d_question
              LEFT JOIN d_user ON d_question.author_id = d_user.id
              LEFT JOIN d_picture ON d_picture.id = d_user.avatar_id
              LEFT JOIN d_poll ON d_question.id = d_poll.question_id """

GROUP_BY = " GROUP BY d_question.id, d_poll.id, d_user.id, d_picture.url"


def get_questions(user_id=None, limit=None, offset=None, extras=None):
    cursor = connection.cursor()

    query = QUERY + extras
    if limit is not None:
        query += " LIMIT %s " % limit
    if offset is not None:
        query += " OFFSET %s " % offset
    cursor.execute(query)
    questions = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return questions, columns


def get_new_questions(limit=None, offset=None, *args, **kwargs):
    extras = GROUP_BY + " ORDER BY d_question.creation_date DESC"
    return get_questions(limit=limit, offset=offset, extras=extras)


def get_popular_questions(limit=None, offset=None, *args, **kwargs):
    extras = GROUP_BY + " ORDER BY likes_count DESC"
    return get_questions(limit=limit, offset=offset, extras=extras)


def get_my_questions(user_id, limit=None, offset=None):
    extras = " WHERE d_question.author_id=%s" % user_id + GROUP_BY + \
             " ORDER BY d_question.creation_date DESC"
    return get_questions(limit=limit, offset=offset, extras=extras)
