import httplib
import json
from django.db import transaction
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import require_post_data
from decider_api.utils.helper import get_short_user_data
from decider_app.models import Question, Comment
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_INVALID_DATA, CODE_UNKNOWN_QUESTION, CODE_CREATED, \
    CODE_SERVER_ERROR


class CommentEndpoint(ProtectedResourceView):

    @transaction.atomic
    @require_post_data(['text', 'question_id'])
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.POST.get('data'))
            text = str(data.get('text')).strip(" ")
            is_anonymous = True if data.get("is_anonymous") is True else False
            question_id = 0

            errors = []
            if not text:
                errors.append('text')
            try:
                question_id = int(data.get("question_id"))
                if not question_id:
                    raise ValueError
            except (ValueError, TypeError):
                errors.append("question_id")

            if errors:
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ["question_id"])

            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return build_error_response(httplib.BAD_REQUEST, CODE_UNKNOWN_QUESTION,
                                            "Question is unknown")

            comment = Comment.objects.create(text=text, question=question, is_anonymous=is_anonymous,
                                             author=request.resource_owner)

            data = {
                "id": comment.id,
                "text": comment.text,
                "creation_date": comment.creation_date,
                "question_id": question.id,
                "is_anonymous": comment.is_anonymous,
                "author": get_short_user_data(request.resource_owner)
            }
            question.comments_count += 1
            question.save()
            return build_response(httplib.CREATED, CODE_CREATED, "Comment added", data=data)

        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_SERVER_ERROR, "Failed to comment")

