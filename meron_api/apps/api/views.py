"""Accept request with image file and return response of face detection function."""
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from meron_api.apps.api.serializers import (FaceDetectionInputSerializer,
                                            FaceDetectionOutputSerializer)


class FaceDetectionResultView(APIView):
    """Accept POST requests with image, call face detection function and return rendered results."""

    def post(self, request):
        """Accept POST request with image either as multipart/form-data or base64 encoded file in JSON."""
        input_serializer = FaceDetectionInputSerializer(data=request.data, context={'request': request})
        if input_serializer.is_valid():
            result = input_serializer.save()

            output_serializer = FaceDetectionOutputSerializer(result)
            return Response(output_serializer.data, status=HTTP_201_CREATED)

        return Response(input_serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Display a message with instructions or disable GET."""
        return Response({'message': 'Please make a POST request with an image'})
