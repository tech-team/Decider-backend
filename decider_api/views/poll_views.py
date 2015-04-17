import httplib
import json
from django.db import transaction
from oauth2_provider.views import ProtectedResourceView
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import require_post_data
from decider_app.models import Vote, Poll, PollItem
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_INVALID_DATA, CODE_CREATED, CODE_UNKNOWN_POLL, \
    CODE_UNKNOWN_POLL_ITEM, CODE_SERVER_ERROR


class PollEndpoint(ProtectedResourceView):

    @transaction.atomic
    @require_post_data(['poll_id', 'poll_item_id'])
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.POST.get('data'))
            p_id = data.get('poll_id')
            pi_id = data.get('poll_item_id')

            try:
                poll = Poll.objects.get(id=p_id)
                pi = PollItem.objects.get(id=pi_id, poll_id=p_id)
            except Poll.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_POLL,
                                            "Poll with specified id was not found")
            except PollItem.DoesNotExist:
                logger.warning("Poll item " + str(pi_id) + " did not match poll " + str(p_id))
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_POLL_ITEM,
                                            "Poll item with specified id was not found")
            except Exception:
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid")

            vote, created = Vote.objects.get_or_create(poll_id=poll.id, poll_item_id=pi.id,
                                                       user=request.resource_owner)
            if created:
                pi.votes_count += 1
                pi.save()
            extra_fields = {'votes_count': pi.votes_count}

            return build_response(httplib.CREATED, CODE_CREATED, "Voted successfully",
                                  extra_fields=extra_fields)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR,
                                        CODE_SERVER_ERROR, "Failed to vote")