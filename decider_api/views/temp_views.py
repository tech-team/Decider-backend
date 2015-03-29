from django.db import connection
from django.http import JsonResponse
from decider_app.models import *

TRUNCATE_QUERY = """
    BEGIN;
    TRUNCATE "comment", "question_likes", "vote", "poll", "category", "question", "comment_likes", "poll_item";
    SELECT setval(pg_get_serial_sequence('"category"','id'), 1, false);
    SELECT setval(pg_get_serial_sequence('"question"','id'), 1, false);
    SELECT setval(pg_get_serial_sequence('"comment"','id'), 1, false);
    SELECT setval(pg_get_serial_sequence('"comment_likes"','id'), 1, false);
    SELECT setval(pg_get_serial_sequence('"poll"','id'), 1, false);
    SELECT setval(pg_get_serial_sequence('"poll_item"','id'), 1, false);
    SELECT setval(pg_get_serial_sequence('"vote"','id'), 1, false);

    COMMIT;
"""


def fill_db(request):
    cur = connection.cursor()
    cur.execute(TRUNCATE_QUERY)
    cur.close()

    try:
        admin_user = User.objects.get(email="admin@admin.com")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser("admin", "admin@admin.com", "admin")

    cat1 = Category.objects.create(name="clothes")
    cat2 = Category.objects.create(name="furniture")

    return JsonResponse({"status": "ok"}, status=201)
