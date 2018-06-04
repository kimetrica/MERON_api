from rest_framework.urls import url

from meron_api.apps.api.views import FaceDetectionResultView


app_name = "api"
urlpatterns = [url(r'^$', FaceDetectionResultView.as_view(), name='api_root'),
               ]
