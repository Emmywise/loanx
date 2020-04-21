from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/(?P<pk>[0-9]+)$',
        views.get_delete_update_borrower,
        name='get_delete_update_borrower'
    ),
    url(
        r'^api/$',
        views.get_post_borrower,
        name='get_post_borrower'
    ),
    url(
        r'^api/(?P<pk>[0-9]+)$',
        views.get_delete_update_borrower_group,
        name='get_delete_update_borrower_group'
    ),
    url(
        r'^api/$',
        views.get_post_borrower_group,
        name='get_post_borrower_group'
    ),
    url(
        r'^api/(?P<pk>[0-9]+)$',
        views.get_delete_update_invite_borrower,
        name='get_delete_update_invite_borrower'
    ),
    url(
        r'^api/$',
        views.get_post_invite_borrower,
        name='get_post_invite_borrower'
    )
]
