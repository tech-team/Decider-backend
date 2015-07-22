import httplib
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from oauth2_provider.views import ProtectedResourceView
from decider_api.utils.endpoint_decorators import require_params
from decider_app.views.utils.response_builder import build_response, build_error_response
from decider_app.views.utils.response_codes import CODE_CREATED, CODE_UNKNOWN_INSTANCE_ID
from push_service.models import GcmClient


class PushAuthEndpoint(ProtectedResourceView):
    @require_params(['instance_id'])
    def post(self, request, *args, **kwargs):

        instance_id = request.POST.get('instance_id')
        reg_token = request.POST.get('reg_token')

        instance, created = GcmClient.objects.get_or_create(instance_id=instance_id)
        instance.registration_token = reg_token
        instance.user = request.resource_owner
        instance.save()

        return build_response(httplib.CREATED, CODE_CREATED, "Authorization successful")


class PushUnauthEndpoint(ProtectedResourceView):
    @require_params(['instance_id'])
    def post(self, request, *args, **kwargs):
        try:
            instance = GcmClient.objects.get(instance_id=request.POST.get('instance_id'))
            instance.delete()
        except ObjectDoesNotExist:
            pass
        return build_response(httplib.CREATED, CODE_CREATED, "Unauthorization successful")


class PushSubEndpoint(ProtectedResourceView):
    @require_params(['instance_id'])
    def post(self, request, *args, **kwargs):
        try:
            instance = GcmClient.objects.get(instance_id=request.POST.get('instance_id'))
            instance.subscribed = True
            instance.save()
        except ObjectDoesNotExist:
            return build_error_response(httplib.BAD_REQUEST, CODE_UNKNOWN_INSTANCE_ID, 'Instance ID unknown')


class PushUnsubEndpoint(ProtectedResourceView):
    @require_params(['instance_id'])
    def post(self, request, *args, **kwargs):
        try:
            instance = GcmClient.objects.get(instance_id=request.POST.get('instance_id'))
            instance.subscribed = False
            instance.save()
        except ObjectDoesNotExist:
            return build_error_response(httplib.BAD_REQUEST, CODE_UNKNOWN_INSTANCE_ID, 'Instance ID unknown')
