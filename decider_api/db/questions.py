from django.db import connection


def tab_switch(case):
    return {
        "new": get_new_questions,
        "popular": get_popular_questions,
        "my": get_my_questions
    }.get(case, None)


QUERY = """SELECT d_question.id, d_question.text, d_question.creation_date,
                  d_question.category_id, d_poll.id,
                  count(DISTINCT d_question_likes.id) as likes_count,
                  count(DISTINCT d_comment.id) as comments_count
           FROM d_question
              LEFT JOIN d_user ON d_question.author_id = d_user.id
              LEFT JOIN d_poll ON d_question.id = d_poll.question_id
              LEFT JOIN d_question_likes ON d_question.id = d_question_likes.question_id
              LEFT JOIN d_comment ON d_question.id = d_comment.question_id"""


def get_questions(user_id=None, limit=None, offset=None, extras=None):
    cursor = connection.cursor()

    query = QUERY + extras
    if limit is not None:
        query += " LIMIT %s " % limit
    if offset is not None:
        query += " OFFSET %s " % offset
    print(query)
    cursor.execute(query)
    questions = cursor.fetchall()
    cursor.close()

    return questions


def get_new_questions(limit=None, offset=None, *args, **kwargs):
    extras = """ GROUP BY d_question.id, d_poll.id
                 ORDER BY d_question.creation_date DESC"""
    return get_questions(limit=limit, offset=offset, extras=extras)


def get_popular_questions(limit=None, offset=None, *args, **kwargs):
    extras = """ GROUP BY d_question.id, d_poll.id
                 ORDER BY likes_count DESC"""
    return get_questions(limit=limit, offset=offset, extras=extras)


def get_my_questions(user_id, limit=None, offset=None):
    extras = """ WHERE d_question.author_id=%s
                 GROUP BY d_question.id, d_poll.id
                 ORDER BY d_question.creation_date DESC""" % user_id
    return get_questions(limit=limit, offset=offset, extras=extras)
