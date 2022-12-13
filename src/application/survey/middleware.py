from django.conf import settings


class MultipleDomainMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        if request.META['HTTP_HOST'] in settings.API_HOSTS:
            request.urlconf = 'application.urls_api'

        if request.META['HTTP_HOST'] in settings.MAPS_HOSTS:
            request.urlconf = 'application.urls_map'

        response = self.get_response(request)

        return response
