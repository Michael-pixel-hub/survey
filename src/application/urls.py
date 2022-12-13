from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include


urlpatterns = [

    path('', include('public_model.urls')),
    path('', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('cache/', include('cache_model.urls')),
    path('sort/', include('sort_model.urls')),
    path('survey/', include('application.survey.urls')),
    path('telegram/', include('application.telegram.urls')),
    path('profi/', include('application.profi.urls')),
    path('agent/', include('application.agent.urls')),
    path('loyalty/', include('application.loyalty.urls')),
    path('mobile/', include('application.mobile.urls')),
    path('iceman/', include('application.iceman.urls')),
    path('iceman/', include('application.iceman_imports.urls')),
    path('users/', include('application.users.urls')),

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
