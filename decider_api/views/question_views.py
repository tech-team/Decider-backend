import httplib
import json
from PIL import Image
import os
import uuid
from django.db import transaction
from django.utils import timezone
from oauth2_provider.views import ProtectedResourceView
from decider_api.db.comments import get_comments
from decider_api.db.poll_items import get_poll_items
from decider_api.db.questions import tab_switch, get_question
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import require_post_data, require_params
from decider_api.utils.helper import get_short_user_data, get_short_user_row_data, str2bool
from decider_api.views.image_views import IMAGE_SIZE, PREVIEW_SIZE
from decider_app.models import Question, Category, User, Poll, PollItem, Picture
from decider_app.views.utils.response_builder import build_response, build_error_response
from decider_app.views.utils.response_codes import *
from decider_backend.settings import MEDIA_ROOT


class QuestionsEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        try:
            tab = request.GET.get('tab')
            limit = request.GET.get('limit')
            offset = request.GET.get('offset')
            categories = request.GET.getlist('categories[]')

            errors = []
            if tab:
                try:
                    tab_func = tab_switch(tab.lower())
                    if tab_func is None:
                        return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_TAB, "Tab is unknown")
                except TypeError:
                    logger.warning("Wrong tab format")
                    return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_TAB, "Tab is unknown")
            else:
                tab_func = tab_switch('new')

            if categories:
                try:
                    for i in range(len(categories)):
                        categories[i] = int(categories[i])
                except (TypeError, ValueError):
                    errors.append('categories')

            if limit:
                try:
                    limit = int(limit)
                except ValueError:
                    errors.append('limit')
            if offset:
                try:
                    offset = int(offset)
                except ValueError:
                    errors.append('offset')

            if errors:
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some parameters are invalid", errors)

            question_list, q_columns = tab_func(user_id=request.resource_owner.id,
                                                limit=limit,
                                                offset=offset,
                                                categories=categories)
            questions = []
            polls = []
            for question_row in question_list:
                poll_id = question_row[q_columns.index('poll_id')]
                if poll_id:
                    polls.append(poll_id)

            poll_items_list, pi_columns = get_poll_items(request.resource_owner.id, polls)

            poll_items = {}
            for poll_item_row in poll_items_list:
                q_id = poll_item_row[pi_columns.index('question_id')]
                pi = {
                    'id': poll_item_row[pi_columns.index('id')],
                    'text': poll_item_row[pi_columns.index('text')],
                    'image_url': poll_item_row[pi_columns.index('image_url')],
                    'preview_url': poll_item_row[pi_columns.index('preview_url')],
                    'votes_count': poll_item_row[pi_columns.index('votes_count')],
                    'voted': True if poll_item_row[pi_columns.index('voted')] else False
                }

                if not poll_items.get(q_id):
                    poll_items[q_id] = []
                poll_items[q_id].append(pi)

            for question_row in question_list:
                poll = poll_items.get(question_row[q_columns.index('id')])
                if poll:
                    poll = sorted(poll, key=lambda k: k['id'])

                question = {
                    'id': question_row[q_columns.index('id')],
                    'text': question_row[q_columns.index('text')],
                    'creation_date': question_row[q_columns.index('creation_date')],
                    'category_id': question_row[q_columns.index('category_id')],
                    'likes_count': question_row[q_columns.index('likes_count')],
                    'comments_count': question_row[q_columns.index('comments_count')],
                    'author': get_short_user_row_data(question_row, q_columns, 'author'),
                    'poll': poll,
                    'is_anonymous': question_row[q_columns.index('is_anonymous')],
                    'voted': True if question_row[q_columns.index('voted')] else False
                }

                questions.append(question)

            extra_fields = {'count': len(questions)}
            return build_response(httplib.OK, CODE_OK, "Successfully fetched questions",
                                  questions, extra_fields)

        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR,
                                        CODE_SERVER_ERROR, "Failed to fetch questions")

    @transaction.atomic
    @require_params(['text', 'category_id'])
    def post(self, request, *args, **kwargs):
        try:
            text = request.POST.get("text")

            try:
                items_count = int(request.POST.get("items_count", 2))
            except (ValueError, TypeError):
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ["items_count"])

            errors = []
            for i in range(1, items_count+1):
                poll_num = "poll_" + str(i)

                if not request.POST.get(poll_num + "_text"):
                    errors.append(poll_num + "_text")
                for field_name in "image", "preview":
                    field = poll_num + "_" + field_name
                    if not request.FILES.get(field):
                        errors.append(field)

            if errors:
                return build_error_response(httplib.BAD_REQUEST, CODE_REQUIRED_PARAMS_MISSING,
                                            "Required params are missing", errors)

            is_anonymous = str2bool(request.POST.get("is_anonymous"))

            try:
                category_id = int(request.POST.get("category_id"))
                if not category_id:
                    raise ValueError
            except (ValueError, TypeError):
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ["category_id"])

            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_CATEGORY, "Category is unknown")

            question = Question.objects.create(text=text, category=category, is_anonymous=is_anonymous,
                                               author=request.resource_owner)
            question_poll = Poll.objects.create(question=question, items_count=items_count)

            data_poll = []
            for i in range(1, items_count+1):
                poll_num = "poll_" + str(i)

                text = request.POST.get(poll_num + '_text')
                image = request.FILES.get(poll_num + '_image')
                preview = request.FILES.get(poll_num + '_preview')

                cur_time = timezone.now().strftime('%s')
                uid = uuid.uuid4().hex
                filename = uid + '.jpg'
                preview_filename = uid + '_preview.jpg'
                dirname = os.path.join('images', 'polls', cur_time[:5], cur_time[5:6])
                url = os.path.join(dirname, filename)
                preview_url = os.path.join(dirname, preview_filename)

                if not os.path.exists(os.path.join(MEDIA_ROOT, dirname)):
                    os.makedirs(os.path.join(MEDIA_ROOT, dirname))

                invalid_fields = []
                try:
                    img = Image.open(image)
                    resize_scale = max(float(img.size[0])/IMAGE_SIZE[0], float(img.size[1])/IMAGE_SIZE[1])
                    if resize_scale > 1:
                        img = img.resize((int(img.size[0]/resize_scale), int(img.size[1]/resize_scale)))
                    img.save(os.path.join(MEDIA_ROOT, url), 'JPEG', quality=95)
                except Exception as e:
                    logger.exception(e)
                    invalid_fields.append(poll_num + '_image')

                try:
                    preview = Image.open(preview)
                    resize_scale = max(float(preview.size[0])/PREVIEW_SIZE[0], float(preview.size[1])/PREVIEW_SIZE[1])
                    if resize_scale > 1:
                        preview = preview.resize((int(preview.size[0]/resize_scale), int(preview.size[1]/resize_scale)))
                    preview.save(os.path.join(MEDIA_ROOT, preview_url), 'JPEG', quality=95)
                except Exception as e:
                    logger.exception(e)
                    invalid_fields.append(poll_num + '_preview')

                if invalid_fields:
                    return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                                "Some fields are invalid", invalid_fields)

                picture = Picture.objects.create(url=os.path.join('media', url), uid=uid,
                                                 preview_url=os.path.join('media', preview_url))

                pi = PollItem.objects.create(poll=question_poll, question=question,
                                             text=text, picture=picture)

                data_poll.append({
                    'id': pi.id,
                    'text': pi.text,
                    'image_url': pi.picture.url if pi.picture else None,
                    'preview_url': pi.picture.preview_url if pi.picture else None,
                    'votes_count': pi.votes_count
                })

            data = {
                "id": question.id,
                "text": question.text,
                "creation_date": question.creation_date,
                "category_id": category.id,
                "author": get_short_user_data(request.resource_owner),
                "poll": data_poll,
                "is_anonymous": question.is_anonymous,
                "likes_count": question.likes_count
            }

            return build_response(httplib.CREATED, CODE_CREATED, "Question added", data)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR,
                                        CODE_SERVER_ERROR, "Failed to create question")


class QuestionDetailsEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        try:

            try:
                q_id = int(kwargs.get("question_id"))
                if not q_id:
                    raise ValueError
            except (ValueError, TypeError):
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ["question_id"])

            question_row, q_columns = get_question(request.resource_owner.id, q_id)
            if question_row is None:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_QUESTION,
                                            "Question with specified id was not found")

            question = {
                'id': question_row[q_columns.index('id')],
                'text': question_row[q_columns.index('text')],
                'creation_date': question_row[q_columns.index('creation_date')],
                'category_id': question_row[q_columns.index('category_id')],
                'author': get_short_user_row_data(question_row, q_columns, 'author'),
                'likes_count': question_row[q_columns.index('likes_count')],
                'is_anonymous': question_row[q_columns.index('is_anonymous')],
                'voted': True if question_row[q_columns.index('voted')] else False
            }

            poll_id = question_row[q_columns.index('poll_id')]
            if poll_id:
                question['poll'] = []
                poll_items_list, pi_columns = get_poll_items(request.resource_owner.id, [poll_id])
                for poll_item_row in poll_items_list:
                    question['poll'].append({
                        'id': poll_item_row[pi_columns.index('id')],
                        'text': poll_item_row[pi_columns.index('text')],
                        'image_url': poll_item_row[pi_columns.index('image_url')],
                        'preview_url': poll_item_row[pi_columns.index('preview_url')],
                        'votes_count': poll_item_row[pi_columns.index('votes_count')],
                        'voted': True if poll_item_row[pi_columns.index('voted')] else False
                    })
                question['poll'] = sorted(question['poll'], key=lambda k: k['id'])
            else:
                question['poll'] = None

            if question_row[q_columns.index('comments_count')] > 0:
                comments = []
                comments_list, c_columns = get_comments(request.resource_owner.id, question['id'])
                for comment_row in comments_list:
                    comments.append({
                        'id': comment_row[c_columns.index('id')],
                        'text': comment_row[c_columns.index('text')],
                        'creation_date': comment_row[c_columns.index('creation_date')],
                        'likes_count': comment_row[c_columns.index('likes_count')],
                        'author': get_short_user_row_data(question_row, q_columns, 'author'),
                        'voted': True if comment_row[c_columns.index('voted')] else False,
                        'is_anonymous': comment_row[c_columns.index('is_anonymous')]
                    })
                question['comments'] = comments
            else:
                question['comments'] = None

            return build_response(httplib.OK, CODE_OK, "Successfully fetched question", data=question)

        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_SERVER_ERROR,
                                        "Failed to get question details")