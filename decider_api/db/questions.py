from django.db import connection


def tab_switch(case):
    return {
        "new": get_new_questions,
        "popular": get_popular_questions,
        "my": get_my_questions
    }.get(case, None)


QUERY = """SELECT d_question.id, d_question.text, d_question.creation_date,
                  d_question.category_id, d_poll.id,
                  count(d_question_likes.id) as likes_count,
                  count(d_comment.id) as comments_count
           FROM d_question
              LEFT JOIN d_user ON d_question.author_id = d_user.id
              LEFT JOIN d_poll ON d_question.id = d_poll.question_id
              LEFT JOIN d_question_likes ON d_question.id = d_question_likes.question_id
              LEFT JOIN d_comment ON d_question.id = d_comment.question_id
           GROUP BY d_question.id, d_poll.id"""


def get_new_questions(user_id=None, limit=None, offset=None):
    cursor = connection.cursor()

    query = QUERY + " ORDER BY d_question.creation_date DESC"
    if limit is not None:
        query += " LIMIT %s " % limit
    if offset is not None:
        query += " OFFSET %s " % offset
    print(query)
    cursor.execute(query)
    questions = cursor.fetchall()
    cursor.close()

    return questions


def get_popular_questions(user_id=None, limit=None, offset=None):
    return 'popular'


def get_my_questions(user_id, limit=None, offset=None):
    return 'my'
