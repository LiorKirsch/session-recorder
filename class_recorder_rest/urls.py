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
#    url(r'^sessions/(?P<session_id>.+)/$', views.RecordingSessionDetailView.as_view()),
#    url(r'^sessions/$', views.RecordingSessionViewSet.as_view()),
    
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
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
    