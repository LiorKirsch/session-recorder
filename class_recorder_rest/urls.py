from django.conf.urls import url, include,patterns
from rest_framework import routers
from class_recorder_rest import views
from django.contrib import admin
from django.conf import settings

from django.contrib import admin
admin.autodiscover()



router = routers.DefaultRouter()
router.register(r'sessions', views.RecordingSessionViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'audios', views.AudioViewSet)
router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^build_slideshow/(?P<session_id>\w{0,20})$', 'class_recorder_rest.views.build_slideshow', name='build_slideshow'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
    