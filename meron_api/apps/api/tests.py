"""Run unittests that make sure API behaves as expected.

The tests that are expecting a result from the API (and not an error) need to be updated as soon as the model is used
instead of the fake function.
"""
import base64
import json
import logging
from tempfile import NamedTemporaryFile

from django.test import Client, SimpleTestCase
from malnutrition_detection import analyze_image

# this is a base64 encoded 1x1 pixel gif
BASE64_ENCODED_GIF = 'R0lGODdhAQABAIAAAP///////ywAAAAAAQABAAACAkQBADs='


class MalnutritionDetectionTestCase(SimpleTestCase):
    """Tests to make sure analyze_image function returns expected results.

    At the moment a fake function is used until the real function is ready. So it doesn't make sense to test expected
    results for specific inputs at the moment.
    """

    def setUp(self):
        """Store objects relevant to all tests in this TestCase.

        - expected return value of malnutrition_detection function
        - image file that can be passed to malnutrition_detection function

        """
        # return from the malnutrition_detection function when both score and classification are calculated.
        # This has to be adjusted to the real function once it's available
        self.complete_return = {'width': 1, 'height': 1, 'score': 1, 'classification': 1}
        # we need to pass a path to analyze_image so we need need a real file on the filesystem
        image_file = NamedTemporaryFile()
        open(image_file.name, 'wb').write(base64.b64decode(BASE64_ENCODED_GIF))
        self.image_file = image_file

    def test_function_returns_expected_result(self):
        """Test a result with all available parameters."""
        result = analyze_image(self.image_file.name, score=True, classification=True)
        self.assertEqual(result, self.complete_return)

    def test_function_returns_result_without_score_if_ommited(self):
        """Test that omitting the score from the input also omits it from the output. classification works the same."""
        result = analyze_image(self.image_file.name, classification=True)
        self.complete_return.pop('score')
        self.assertEqual(result, self.complete_return)


class MERONApiTestCase(SimpleTestCase):
    """TestCase to test the API itself. SimpleTestCase so DB isn't setup, we aren't using one at the moment."""

    def setUp(self):
        """Store objects relevant to all tests in this TestCase.

        - expected return value of malnutrition_detection function
        - image file that can be passed to the API as multipart/form-data
        - image file as base64 encoded string that that can be passed to the API as JSON

        """
        self.complete_return = {'width': 1, 'height': 1, 'score': 1, 'classification': 1}
        self.base64_image_string = BASE64_ENCODED_GIF
        image_file = NamedTemporaryFile()
        with open(image_file.name, 'wb') as open_image_file:
            open_image_file.write(base64.b64decode(BASE64_ENCODED_GIF))
        self.image_file = image_file
        self.client = Client()
        # disable logging to have clean test run output
        logging.disable(logging.CRITICAL)

    def test_post_to_api_with_base64_in_json(self):
        """Test that a POST request with a valid image file as base64 encoded string in JSON works as expected."""
        res = self.client.post('/', data=json.dumps({'image': self.base64_image_string}),
                               content_type='application/json')
        self.complete_return.pop('score')
        self.complete_return.pop('classification')
        self.assertEquals(res.json(), self.complete_return)

    def test_post_to_api_with_formdata(self):
        """Test that a POST request with a valid image file as multipart/form-data works as expected."""
        res = self.client.post('/', data={'image': self.image_file})
        self.complete_return.pop('score')
        self.complete_return.pop('classification')
        self.assertEquals(res.json(), self.complete_return)

    def test_post_json_to_api_with_score(self):
        """Test that a POST request with valid image as JSON and `"score": true` works as expected."""
        res = self.client.post('/', data=json.dumps({'image': self.base64_image_string, 'score': True}),
                               content_type='application/json')
        self.complete_return.pop('classification')
        self.assertEquals(res.json(), self.complete_return)

    def test_post_json_without_image_key_fails(self):
        """Test that a POST request without an image file fails as expected."""
        res = self.client.post('/', data=json.dumps({'no_image': ''}),
                               content_type='application/json')
        self.assertEquals(res.status_code, 400)
        self.assertEquals(res.json()['image'], ['No file was submitted.'])

    def test_post_json_with_non_image_base64_string_fails(self):
        """Test that a POST request with an invalid image file as base64 encoded string fails as expected."""
        res = self.client.post('/', data=json.dumps({'image': "I'm no image"}),
                               content_type='application/json')
        self.assertEquals(res.status_code, 400)
        self.assertEquals(res.json()['image'],
                          ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
                          )

    def test_post_formdata_with_invalid_image_file_fails(self):
        """Test that a POST request with an invalid image file as multipart/form-data fails as expected."""
        with open(self.image_file.name, 'wb') as open_image_file:
            open_image_file.write(b'no image')
        res = self.client.post('/', data={'image': self.image_file})
        self.assertEquals(res.status_code, 400)
        self.assertEquals(res.json()['image'],
                          ['Upload a valid image. The file you uploaded was either not an image or a corrupted image.']
                          )

    def test_post_formdata_with_empty_image_file_fails(self):
        """Test that a POST request with an empty image fail as multipart/form-data fails as expected."""
        with open(self.image_file.name, 'wb'):
            pass
        res = self.client.post('/', data={'image': self.image_file})
        self.assertEquals(res.status_code, 400)
        self.assertEquals(res.json()['image'], ['The submitted file is empty.'])
