from django.conf.urls import url
from django.urls import path, include
from . import views
# from .views import BorrowerFileList, BorrowerFileDetail


urlpatterns = [
    url(
        r'^api/(?P<pk>[0-9]+)/$',
        views.get_delete_update_staff,
        name='get_delete_update_staff'
    ),
    url(
        r'^api/$',
        views.get_post_staff,
        name='get_post_staff'
    )
]
