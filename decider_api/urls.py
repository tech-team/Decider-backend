from django.conf.urls import url, patterns, include
from decider_api.views import auth_views, temp_views
from decider_api.views.category_views import CategoriesEndpoint
from decider_api.views.comment_views import CommentsEndpoint
from decider_api.views.image_views import ImagesEndpoint
from decider_api.views.poll_views import PollEndpoint
from decider_api.views.question_views import QuestionsEndpoint, QuestionDetailsEndpoint
from decider_api.views.user_data_views import UserDataEndpoint, UserEditEndpoint
from decider_api.views.vote_views import VoteEndpoint

urlpatterns = patterns('',
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^login/?$', auth_views.login_view, name="login"),
    url(r'^registration/?$', auth_views.registration_view, name="registration"),
    url(r'^refresh_token/?$', auth_views.refresh_token_view, name="refresh_token"),

    url(r'^user/(?P<user_id>[0-9]+)/?$', UserDataEndpoint.as_view(), name="user"),
    url(r'^edit/?$', UserEditEndpoint.as_view(), name="edit"),

    url(r'^questions/?$', QuestionsEndpoint.as_view(), name="questions"),
    url(r'^questions/(?P<question_id>[0-9]+)/?$', QuestionDetailsEndpoint.as_view(), name="question"),
    url(r'^poll/?$', PollEndpoint.as_view(), name="poll"),
    url(r'^images/?$', ImagesEndpoint.as_view(), name="images"),
    url(r'^categories/?$', CategoriesEndpoint.as_view(), name="categories"),
    url(r'^comments/?$', CommentsEndpoint.as_view(), name="comments"),
    url(r'^vote/?$', VoteEndpoint.as_view(), name="vote"),

    url(r'^logout/?$', auth_views.logout_view, name="logout_view"),

    # TODO: remove tmp
    url(r'^tmp/fill_db/?$', temp_views.fill_db, name="fill_db"),
    url(r'^tmp/delete_entity/?$', temp_views.delete_entity, name="delete_question")
)
