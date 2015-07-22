from django.db import connection
from django.utils import timezone
from decider_app.views.utils.response_codes import I_CODE_UNKNOWN_ENTITY, I_CODE_NO_MATCH, I_CODE_ALREADY_VOTED, \
    I_CODE_VOTE_OK

SELECT_QUERY = """
                  SELECT d_poll_item.id as pi_id,
                         d_poll.id as p_id,
                         d_vote.id as voted
                  FROM d_poll_item
                  LEFT JOIN d_poll ON d_poll.id=d_poll_item.poll_id
                  LEFT JOIN d_vote ON d_vote.poll_id=d_poll.id AND d_vote.user_id={0}
                  WHERE d_poll_item.id={1}
               """

INSERT_QUERY = """INSERT INTO d_vote (user_id, poll_id, poll_item_id, creation_date) values({0}, {1}, {2}, {3})"""

UPDATE_QUERY = """UPDATE d_poll_item
                  SET votes_count = votes_count + 1
                  WHERE id={0}"""

VOTES_QUERY = """SELECT d_poll_item.id, votes_count
                  FROM d_poll
                  LEFT JOIN d_poll_item ON d_poll_item.poll_id = d_poll.id
                  WHERE d_poll.id={0}
                  ORDER BY d_poll_item.id"""


def check_poll_item(user_id, p_id, pi_id):
    cursor = connection.cursor()

    query = SELECT_QUERY.format(user_id, pi_id)
    cursor.execute(query)
    res = cursor.fetchone()
    if not res:
        return I_CODE_UNKNOWN_ENTITY
    elif p_id != res[1]:
        return I_CODE_NO_MATCH
    elif res[2]:
        return I_CODE_ALREADY_VOTED
    else:
        return I_CODE_VOTE_OK


def vote_on_poll(user_id, poll_id, poll_item_id):
    cursor = connection.cursor()

    query = INSERT_QUERY.format(user_id, poll_id, poll_item_id, timezone.now())
    cursor.execute(query)

    query = UPDATE_QUERY.format(poll_item_id)
    cursor.execute(query)

    query = VOTES_QUERY.format(poll_id)
    cursor.execute(query)
    res = cursor.fetchall()

    return res