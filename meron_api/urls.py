"""We are going to define most urls in apps."""
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    url(r"", include("meron_api.apps.api.urls", namespace="api")),
    url(r"frontend/", include("meron_api.apps.frontend.urls", namespace="frontend")),
]


if settings.DEBUG:
    # we only install debug_toolbar in development mode, but we might choose to temporarily run with DEBUG=True in
    # other modes to debug issues, that shouldn't fail because debug_toolbar is not installed.
    try:
        import debug_toolbar

        urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ModuleNotFoundError:
        pass
