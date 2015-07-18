import httplib
import json
from django.db import transaction
from oauth2_provider.views import ProtectedResourceView
from decider_api.db.comments import get_comments
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import require_post_data, require_params
from decider_api.utils.helper import get_short_user_data, RepresentsInt, check_params_types, get_short_user_row_data, \
    str2bool
from decider_app.models import Question, Comment
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_INVALID_DATA, CODE_UNKNOWN_QUESTION, CODE_CREATED, \
    CODE_SERVER_ERROR, CODE_OK


class CommentsEndpoint(ProtectedResourceView):

    ALLOWED_ORDER_FIELDS = ['creation_date', '-creation_date']

    @require_params(['question_id'])
    def get(self, request, *args, **kwargs):
        params = {
            'question_id': request.GET.get('question_id'),
            'limit': request.GET.get('limit'),
            'offset': request.GET.get('offset')
        }

        errors = check_params_types(params, int)

        order = request.GET.get('order')
        if order and order in self.ALLOWED_ORDER_FIELDS:
            if order.startswith('-'):
                order = order[1:] + " desc"
            else:
                order += " asc"
        else:
            order = "creation_date desc"

        if errors:
            return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                        "Some fields are invalid", errors)

        comments_list, c_columns = get_comments(request.resource_owner.id, params['question_id'],
                                                order=order,
                                                limit=params['limit'], offset=params['offset'])
        comments = []
        for comment_row in comments_list:
            comments.append({
                'id': comment_row[c_columns.index('id')],
                'text': comment_row[c_columns.index('text')],
                'creation_date': comment_row[c_columns.index('creation_date')],
                'likes_count': comment_row[c_columns.index('likes_count')],
                'author': get_short_user_row_data(comment_row, c_columns, 'author'),
                'voted': True if comment_row[c_columns.index('voted')] else False,
                'is_anonymous': comment_row[c_columns.index('is_anonymous')],
                'question_id': comment_row[c_columns.index('question_id')]
            })

        return build_response(httplib.OK, CODE_OK, "Successfully fetched comments", data=comments)

    @transaction.atomic
    @require_post_data(['text', 'question_id'])
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.POST.get('data'))
            text = str(data.get('text')).strip(" ")
            is_anonymous = str2bool(data.get("is_anonymous"))
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

            comment = Comment.objects.create(text=text, question=question,
                                             is_anonymous=is_anonymous,
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

