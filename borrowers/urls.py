from django.conf.urls import url
from . import views
from django.urls import path, include
from .views import BorrowerFileList, BorrowerFileDetail

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
        r'^api/group/(?P<pk>[0-9]+)$',
        views.get_delete_update_borrower_group,
        name='get_delete_update_borrower_group'
    ),
    url(
        r'^api/group/$',
        views.get_post_borrower_group,
        name='get_post_borrower_group'
    ),
    url(
        r'^api/add-to-group/$',
        views.add_to_group,
        name='add_to_group'
    ),
    url(
        r'^api/invite/(?P<pk>[0-9]+)$',
        views.get_delete_update_invite_borrower,
        name='get_delete_update_invite_borrower'
    ),
    url(
        r'^api/invite/$',
        views.get_post_invite_borrower,
        name='get_post_invite_borrower'
    ),
    path('api/attachments/',
        BorrowerFileList.as_view()
    ),
    path('api/attachments/<int:pk>/',
        BorrowerFileDetail.as_view()
    )
]
