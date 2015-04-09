import httplib
from oauth2_provider.views import ProtectedResourceView
from decider_api.db.categories import get_categories
from decider_api.utils.endpoint_decorators import require_get_params
from decider_app.models import Locale
from decider_app.views.utils.response_builder import build_response
from decider_app.views.utils.response_codes import CODE_OK


class CategoriesEndpoint(ProtectedResourceView):
    @require_get_params(['locale'])
    def get(self, request, *args, **kwargs):

        try:
            locale = Locale.objects.get(name=request.GET.get('locale'))
        except Locale.DoesNotExist:
            locale = Locale.objects.get(name="ru_RU")

        categories_row, columns = get_categories(locale.id)

        data = []
        for category in categories_row:
            data.append({
                'id': category[columns.index('id')],
                'name': category[columns.index('name')]
            })

        extra_fields = {
            'total': len(categories_row),
            'locale': locale.name
        }

        return build_response(httplib.OK, CODE_OK, "Successfully fetched categories",
                              data, extra_fields=extra_fields)