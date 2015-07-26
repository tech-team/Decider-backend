import httplib
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.shortcuts import render
from oauth2_provider.views import ProtectedResourceView
from decider_api.utils.endpoint_decorators import track_activity, require_params
from decider_app.models import Question, SpamReport
from decider_app.views.utils.response_builder import build_error_response, build_response
from decider_app.views.utils.response_codes import CODE_UNKNOWN_ENTITY, CODE_INVALID_ENTITY, CODE_CREATED


class SpamEndpoint(ProtectedResourceView):

    @require_params(['entity', 'entity_id'])
    @track_activity
    def post(self, request, *args, **kwargs):
        entity = request.POST.get('entity')
        entity_id = int(request.POST.get('entity_id'))

        if entity not in ['comment', 'question']:
            return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_ENTITY, "Invalid entity")

        try:
            ent = get_model('decider_app', entity).objects.get(id=entity_id)
            vote, created = SpamReport.objects.get_or_create(entity=entity, entity_id=entity_id,
                                                             user=request.resource_owner)
        except ObjectDoesNotExist:
            return build_error_response(httplib.BAD_REQUEST, CODE_UNKNOWN_ENTITY, "Unknown entity")

        if created:
            ent.spam_count += 1
            ent.is_active = True if ent.spam_count < 5 else False
            ent.save()

        return build_response(httplib.CREATED, CODE_CREATED, "Marked successfully")
