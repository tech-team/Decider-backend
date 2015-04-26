import httplib
import json
from django.db import transaction, IntegrityError
from oauth2_provider.views import ProtectedResourceView
from decider_api.db.poll import vote_on_poll, check_poll_item
from decider_api.log_manager import logger
from decider_api.utils.endpoint_decorators import require_post_data
from decider_app.models import Vote, Poll, PollItem
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_INVALID_DATA, CODE_CREATED, CODE_UNKNOWN_POLL, \
    CODE_UNKNOWN_POLL_ITEM, CODE_SERVER_ERROR, CODE_UNKNOWN_POLL_DATA, CODE_ALREADY_VOTED, I_CODE_UNKNOWN_ENTITY, \
    I_CODE_NO_MATCH, I_CODE_ALREADY_VOTED


class PollEndpoint(ProtectedResourceView):

    @transaction.atomic
    @require_post_data(['poll_id', 'poll_item_id'])
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.POST.get('data'))

            user_id = request.resource_owner.id
            p_id = data.get('poll_id')
            pi_id = data.get('poll_item_id')

            res_code = check_poll_item(user_id, p_id, pi_id)

            if res_code == I_CODE_UNKNOWN_ENTITY:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_POLL_ITEM,
                                            "Poll item with specified id was not found")
            elif res_code == I_CODE_NO_MATCH:
                logger.warning("Poll item " + str(pi_id) + " did not match poll " + str(p_id))
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_POLL,
                                            "Poll with specified id was not found")
            elif res_code == I_CODE_ALREADY_VOTED:
                return build_error_response(httplib.FORBIDDEN, CODE_ALREADY_VOTED,
                                            "Already voted for that poll")

            votes_count = vote_on_poll(user_id, p_id, pi_id)

            extra_fields = {'votes_count': votes_count}

            return build_response(httplib.CREATED, CODE_CREATED, "Voted successfully",
                                  extra_fields=extra_fields)
        except Exception as e:
            logger.exception(e)
            return build_error_response(httplib.INTERNAL_SERVER_ERROR,
                                        CODE_SERVER_ERROR, "Failed to vote")