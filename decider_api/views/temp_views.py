from django.db import connection
from django.http import JsonResponse
from decider_app.models import *


def truncate_all():
    Question.objects.all().delete()
    Comment.objects.all().delete()
    CommentLike.objects.all().delete()
    Country.objects.all().delete()
    Category.objects.all().delete()
    Picture.objects.all().delete()


def fill_db(request):
    truncate_all()

    try:
        admin_user = User.objects.get(email="admin@admin.com")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser("admin", "admin@admin.com", "admin")

    country1 = Country.objects.create(name="Russland")

    picture1 = Picture.objects.create(url="see.com")
    picture2 = Picture.objects.create(url="sieben.com")

    cat1 = Category.objects.create(name="clothes")
    cat2 = Category.objects.create(name="furniture")

    try:
        user1 = User.objects.get(email="snake@snake.snake")
    except User.DoesNotExist:
        user1 = User.objects.create(username="snake", email="snake@snake.snake", country=country1)
        user1.set_password("snake")
        user1.save()
    try:
        user2 = User.objects.get(email="aaa@aaa.aaa")
    except User.DoesNotExist:
        user2 = User.objects.create(username="aaa", email="aaa@aaa.aaa", country=country1)
        user2.set_password("aaa")
        user2.save()

    q1 = Question.objects.create(text="Question1", author=user1, category=cat1)
    q2 = Question.objects.create(text="Question2", author=user1, category=cat2)
    q3 = Question.objects.create(text="Question3", author=admin_user, category=cat2)

    q1.likes.add(user1)
    q1.likes.add(admin_user)
    q1.likes.add(user2)
    q2.likes.add(admin_user)

    poll1 = Poll.objects.create(question=q1)
    poll2 = Poll.objects.create(question=q2)

    pi1 = PollItem.objects.create(poll=poll1, question=q1, text="pi1", picture=picture1)
    pi2 = PollItem.objects.create(poll=poll1, question=q1, text="pi2")
    pi3 = PollItem.objects.create(poll=poll2, question=q2, text="pi3")
    pi4 = PollItem.objects.create(poll=poll2, question=q2, text="pi4", picture=picture2)
    pi5 = PollItem.objects.create(poll=poll2, question=q2, text="pi5")

    comm1 = Comment.objects.create(question=q1, author=user1, text="hallo")
    comm2 = Comment.objects.create(question=q1, author=admin_user, text="auf wiedersehen")
    comm3 = Comment.objects.create(question=q3, author=admin_user, text="auf wiedersehen")

    return JsonResponse({"status": "ok"}, status=201)
