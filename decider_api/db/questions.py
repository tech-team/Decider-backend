from django.db import connection


def tab_switch(case):
    return {
        "new": get_new_questions,
        "popular": get_popular_questions,
        "my": get_my_questions
    }.get(case, None)

QUERY = """SELECT d_question.id, d_question.text, d_question.creation_date, d_question.is_active,
                  d_question.category_id, d_poll.id as poll_id, d_question.author_id,
                  d_question.likes_count, d_question.comments_count, d_question.is_anonymous,
                  d_user.first_name as author_first_name, d_user.last_name as author_last_name,
                  d_user.middle_name as author_middle_name, d_user.username as author_username,
                  d_user.uid as author_uid, d_picture.url as author_image_url,
                  d_user.is_anonymous as author_anonymous, d_question_likes.id as voted,
                  (likes_count + d_question.comments_count + sum(d_poll_item.votes_count)) as popularity
           FROM d_question
              LEFT JOIN d_user ON d_question.author_id = d_user.id
              LEFT JOIN d_picture ON d_picture.id = d_user.avatar_id
              LEFT JOIN d_poll ON d_question.id = d_poll.question_id
              LEFT JOIN d_question_likes ON d_question_likes.question_id = d_question.id
                                        AND d_question_likes.user_id = {}
              LEFT JOIN d_poll_item ON d_poll_item.poll_id = d_poll.id"""



WHERE = " WHERE d_question.is_active=TRUE"

GROUP_BY = " GROUP BY d_question.id, d_poll.id, d_user.id, d_picture.url, d_question_likes.id"


def get_questions(*args, **kwargs):
    cursor = connection.cursor()
    where = WHERE
    fqid = kwargs.get('first_question_id')
    if fqid > -1:
        where += " AND d_question.id < {0}".format(fqid)

    query = QUERY.format(kwargs.get('user_id')) + where
    if kwargs.get('categories'):
        category_ids = (', '.join([str(x) for x in kwargs.get('categories')]))
        query += ' AND d_question.category_id IN (%s)' % category_ids
    if kwargs.get('where'):
        for item in kwargs.get('where'):
            query += ' AND' + item

    if kwargs.get('extras'):
        query += kwargs.get('extras')

    if kwargs.get('limit') is not None:
        query += " LIMIT %s " % kwargs.get('limit')
    if kwargs.get('offset') is not None:
        query += " OFFSET %s " % kwargs.get('offset')

    cursor.execute(query)
    questions = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return questions, columns


def get_new_questions(*args, **kwargs):
    extras = GROUP_BY + " ORDER BY d_question.creation_date DESC"
    return get_questions(user_id=kwargs.get('user_id'),
                         limit=kwargs.get('limit'), offset=kwargs.get('offset'),
                         categories=kwargs.get('categories'), extras=extras,
                         first_question_id=kwargs.get('first_question_id'))


def get_popular_questions(*args, **kwargs):
    extras = GROUP_BY + " ORDER BY popularity DESC"
    return get_questions(user_id=kwargs.get('user_id'),
                         limit=kwargs.get('limit'), offset=kwargs.get('offset'),
                         categories=kwargs.get('categories'), extras=extras)


def get_my_questions(*args, **kwargs):
    where = [" d_question.author_id=%s" % kwargs.get('user_id')]
    extras = GROUP_BY + " ORDER BY d_question.creation_date DESC"
    return get_questions(user_id=kwargs.get('user_id'),
                         limit=kwargs.get('limit'), offset=kwargs.get('offset'),
                         categories=kwargs.get('categories'), where=where, extras=extras,
                         first_question_id=kwargs.get('first_question_id'))


def get_question(user_id, q_id):
    extras = " WHERE d_question.id=%s" % q_id + GROUP_BY
    cursor = connection.cursor()
    cursor.execute(QUERY.format(user_id) + extras)
    question = cursor.fetchone()
    columns = [i[0] for i in cursor.description]
    cursor.close()

    return question, columns