import httplib
import json
from oauth2_provider.views import ProtectedResourceView
from decider_app.models import Question, Category, User, Poll, PollItem
from decider_app.views.utils.response_builder import build_response, build_error_response
from decider_app.views.utils.response_codes import CODE_INVALID_DATA, CODE_UNKNOWN_CATEGORY, CODE_CREATED


class NewQuestionEndpoint(ProtectedResourceView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.POST.get("data"))
            text = data.get("text")
            poll = data.get("poll")
            category_id = 0
            is_anonymous = data.get("is_anonymous") if data.get("is_anonymous") else False

            errors = []
            if not text:
                errors.append("text")
            if not poll:
                errors.append("poll")
            try:
                category_id = int(data.get("category_id"))
                if not category_id:
                    raise ValueError
            except (ValueError, TypeError):
                errors.append("category_id")

            if errors:
                return build_error_response(httplib.BAD_REQUEST, CODE_UNKNOWN_CATEGORY,
                                            "Some fields are invalid", errors)

            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_CATEGORY, "Category is unknown")

            question = Question.objects.create(text=text, category=category, is_anonymous=is_anonymous,
                                               author=request.resource_owner)
            question_poll = Poll.objects.create(question=question)

            data_poll = []
            for poll_item in poll:
                text = poll_item.get('text')
                image_url = ""  # TODO: get image from poll_item.image

                if not text:
                    return build_error_response(httplib.BAD_REQUEST, CODE_UNKNOWN_CATEGORY,
                                                "Some fields are invalid", ["poll_item.text"])

                pi = PollItem.objects.create(poll=question_poll, question=question,
                                             text=poll_item['text'], image_url=image_url)
                data_poll.append({
                    'id': pi.id,
                    'text': pi.text,
                    'image_url': pi.image_url
                })

            author = {
                "id": request.resource_owner.id,
                "username": request.resource_owner.username,
                "last_name": request.resource_owner.last_name,
                "first_name": request.resource_owner.first_name,
                "avatar": request.resource_owner.avatar_url
            }

            data = {
                "id": question.id,
                "text": question.text,
                "creation_date": question.creation_date,
                "category_id": category.id,
                "author": author,
                "poll": data_poll,
                "is_anonymous": question.is_anonymous
            }

            return build_response(httplib.CREATED, CODE_CREATED, "Question added", data)
        except Exception as e:
            print(e)
            # TODO: write to log
            return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA, "Failed to create question")
