from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('v1/survey/', include('application.survey.urls_api')),
    path('v1/iceman/', include('application.iceman.urls_api')),
    path('v1/profi/', include('application.profi.urls_api')),
    path('v1/agent/', include('application.agent.urls_api')),
    path('v1/loyalty/', include('application.loyalty.urls_api')),
    path('', RedirectView.as_view(url='/v1/survey/')),
    path('v1/', RedirectView.as_view(url='/v1/survey/')),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar
if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
