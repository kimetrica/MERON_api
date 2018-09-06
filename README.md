# MERON API

This project provides a REST API based on [django-restframework](http://www.django-rest-framework.org/) for the [malnutrition detection](https://github.com/kimetrica/meron_production) project.
Currently the API is very simple. It provides an endpoint where images can be submitted along with appropriate meta-data via a POST request. It will then return a `JSON` representation of the result which can include a malnutrition classification or weight-for-height (or weight-for-length) z-score.


## Important Note
Our current focus of development has been on the model for predicting malnutrition classification. Although we provide a model for calculating weight-for-height (or weight-for-length) z-score this should be considered early beta and results should be used with caution. If you request both a score and a classification, you may find that the score contradicts the classification for diagnosing malnutrition. In this case, the classification should be considered more reliable.

The models have been developed with a limited scope of training data. We are working towards collecting more data to improve the results of both the score and classification models.


## How to Use the API
Malnutrition classification and score can be obtained by POSTing an image, age (months), and gender to the API.

To POST an image to the API, you have two options:

-   You can do a regular `multipart/form-data` request that transmits the image like a HTML file upload.
-   You can do an `application/json` request, and include the image as a base64 encoded string. The API will accept both. base64-encoding the file will add approximately 30% to the file-size, so if data volume or connection speed are of concern a `multipart/form-data` request might be preferable.

The endpoint accepts two optional boolean arguments, `score` and `classification`. If instructed via those arguments, the function will calculate and include those parameters in the result. Those parameters can either be passed in the request body or provided via GET parameters in the URL.

In addition, the API also requires the parameters `age` and `gender` in the request body, where `gender` is expected to be either `m` or `f` and age is an integer. The age should be the age of the subject in months.

## Trying the API

The API ships with a very simple page that allows you to upload a file using a [HTML form](/frontend/)

### Example Data Parameters

    {
        'image' : [base64 encoded string],
        'score' : Boolean (Default is True),
        'classification' : Boolean (Default is True),
        'age' : integer (age in months),
        'gender' : string ('m' or 'f')
    }


## Example POST requests to the MERON api

The following examples demonstrate how to make an API request to the MERON API (assumed to be running locally). Replace `http://meron.localdomain` with `http://localhost:8000` when running in development mode.


### curl command for posting an image as multipart/form-data with score and classification calculation (score set via body and classification via GET parameter for the sake of demonstration)

`curl -v  -F "score=true" -F "image=@example_image.jpeg" http://meron.localdomain?classification`


### curl command for posting a base64 encoded image in a JSON object

`(echo -n '{"image": "'; base64 example_image.jpeg; echo '", "classification": true, "age": 30, "gender": "'f'"}') | curl -v -H 'content-type: application/json' -d @- http://meron.localdomain?classification
`


### Python example using the requests library (multipart/form-data)

    import requests

    res = requests.post('http://meron.localdomain?classification', files={'image': open('example_image.jpeg', 'rb')}, data={'classification': True, "age": 30, "gender": 'f'})


### Python example using the requests library (base64 encoded image)

    from base64 import b64encode
    import requests


    with open('example_image.jpeg', 'rb') as image_file:
        encoded_string = b64encode(image_file.read())

    # we need to decode the byte-string returned by b64encode so it's JSON serializable
    res = requests.post('http://meron.localdomain?classification', json={'image': encoded_string.decode(), 'classification': True, "age": 30, "gender": 'f'})


## Running the project

The API setup is based on Docker. You can use the provided docker-compose files to run it either in a production-like configuration (using a copy of the production settings without HTTPS) or in development mode, where it will mount the source code directory as a read-only folder so changes are picked up immediately by the development webserver.

To run in production mode issue the following command:

`docker-compose -f docker-compose.yml up`


The `docker-compose.yml` file has to be passed explicitly because otherwise _docker-compose_ will automatically load the `docker-compose.override.yml` file which is intended for development.

To run in development mode simply run this command:

`docker-compose up`

It is also possible to run the development server without Docker. Just do the following steps:

1.  Create a virtual environment, e.g. `python -m venv ~/.venvs/meron_api`
2.  Activate the environment: `source ~/.venvs/meron_api`
3.  Install the development dependencies: `pip install -r meron_api/requirements/development.txt`
4.  Start the development server: `python manage.py runserver[_plus]`

To access the locally running copy of the API, you can use `localhost:8000` in development mode. In production mode, it is necessary to add an entry to your `hosts` file that resolves a domain to the IP Docker uses: `172.33.0.2       meron.localdomain`.
Now you can access the API running on your local computer under: [http://meron.localdomain](http://meron.localdomain).
