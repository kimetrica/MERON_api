"""Accept request with image file and return response of face detection function."""
import markdown

from meron_api.apps.api.serializers import (
    FaceDetectionInputSerializer,
    FaceDetectionOutputSerializer,
)
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class FaceDetectionResultView(APIView):
    """Accept POST requests with image, call face detection function and return rendered results."""

    def get_renderers(self):
        """Override renderers if we are dealing with a GET request.

        DEFAULT_RENDERER_CLASSES are JSONRenderer and ReadOnlyBrowsableAPIRenderer.
        If a browser opens the index page, we want to display the README.md as
        HTML instead of the API browser
        """
        request = self.get_renderer_context()["request"]
        if request.method == "GET":
            return [JSONRenderer(), StaticHTMLRenderer()]
        return [renderer() for renderer in self.renderer_classes]

    def post(self, request):
        """Accept POST request with image either as multipart/form-data or base64 encoded file in JSON."""
        # passing the request to the context so we can access the query_params
        input_serializer = FaceDetectionInputSerializer(
            data=request.data, context={"request": request}
        )
        if input_serializer.is_valid():
            result = input_serializer.save()

            output_serializer = FaceDetectionOutputSerializer(result)
            return Response(output_serializer.data, status=HTTP_201_CREATED)

        return Response(input_serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Display a rendered version of README.md for browsers.

        Other clients (e.g. curl) should see a message about usage.
        """
        if request.accepted_renderer.format == "html":
            md = open("README.md").read()
            rendered_html = markdown.markdown(md)
            html = """<!DOCTYPE html>
                      <html>
                      <head>
                      <meta charset="UTF-8">
                      <title>MERON API</title>
                      </head>
                      <body>
                      {}
                      </body>
                      </html>
                   """.format(
                rendered_html
            )
            return Response(html)

        msg = (
            "Please make a POST request with an image. Other paramters are "
            "'score' (Boolean, default True), 'classification' (Boolean, "
            "default True), 'age' (Integer, age in months), 'gender' (String"
            ", 'm' or 'f')"
        )
        return Response({"message": msg})
