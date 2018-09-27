# MERON API

This project provides a REST API based on [django-restframework](http://www.django-rest-framework.org/) for the [malnutrition detection](https://github.com/kimetrica/meron_production) project.


## Source code

The source code repository for this API can be found here: [https://github.com/kimetrica/meron](https://github.com/kimetrica/meron)


## Live version of the API
You can find a live version of the API here: [https://meron.kimetrica.com/](https://meron.kimetrica.com/)


## API frontend

There is a simple HTML frontend that can be used to submit an image to the API for testing purposes: [https://meron.kimetrica.com/frontend/](https://meron.kimetrica.com/frontend/)


## About the API

Currently the API is very simple. It provides an endpoint where images can be submitted along with appropriate meta-data via a POST request. It will then return a `JSON` representation of the result which can include a malnutrition classification or weight-for-height (or weight-for-length) z-score.


## Important Note
Our current focus of development has been on the model for predicting malnutrition classification. Although we provide a model for calculating weight-for-height (or weight-for-length) z-score this should be considered early beta and results should be used with caution. If you request both a score and a classification, you may find that the score contradicts the classification for diagnosing malnutrition. In this case, the classification should be considered more reliable.

The models have been developed with a limited scope of training data. We are working towards collecting more data to improve the results of both the score and classification models.


## Using the API
Malnutrition classification and score can be obtained by POSTing an image, age (months), and gender to the API.

To POST an image to the API, you have two options:

-   You can do a regular `multipart/form-data` request that transmits the image like a HTML file upload.
-   You can do an `application/json` request, and include the image as a base64 encoded string. The API will accept both. base64-encoding the file will add approximately 30% to the file-size, so if data volume or connection speed are of concern a `multipart/form-data` request might be preferable.

The endpoint accepts two optional boolean arguments, `score` and `classification`, that can be used to omit either value from the result. To return only the score, you can pass `"classification": false` in the request body and vice versa.

In addition, the API also requires the parameters `age` and `gender` in the request body, where `gender` is expected to be either `m` or `f` and age is an integer. The age should be the age of the subject in months.


### Example Data Parameters

    {
        'image' : [base64 encoded string],
        'score' : Boolean (Default is True),
        'classification' : Boolean (Default is True),
        'age' : integer (age in months),
        'gender' : string ('m' or 'f')
    }


## Example POST requests to the MERON api

The following examples demonstrate how to make an API request to the MERON API. Replace `https://meron.kimetrica.com/` with `http://meron.localdomain` when running in development mode (see below for setup instructions).


### curl for posting an image as multipart/form-data, omitting classification

`curl -F "classification=false" -F "image=@face.jpg" -F "age=30" -F "gender=m" https://meron.kimetrica.com/`


### curl for posting a base64 encoded image, omitting score

`(echo -n '{"image": "'; base64 face.jpg; echo '", "score": false, "age": 30, "gender": "m"}') | curl -H 'content-type: application/json' -d @- https://meron.kimetrica.com/`


### Python example using requests library (multipart/form-data), omitting classification

    import requests


    res = requests.post(
        "https://meron.kimetrica.com/",
        files={"image": open("face.jpg", "rb")},
        data={"classification": False, "age": 30, "gender": "m"},
    )
    print(res.json())


### Python example using requests library (base64 encoded image), omitting score

    from base64 import b64encode
    import requests


    with open("face.jpg", "rb") as image_file:
        encoded_string = b64encode(image_file.read())

    # we need to decode the byte-string returned by b64encode so it's JSON serializable
    res = requests.post(
        "https://meron.kimetrica.com/",
        json={"image": encoded_string.decode(), "score": False, "age": 30, "gender": "m"},
    )
    print(res.json())


## Running the project locally

The API setup is based on Docker containers. You can use the provided docker-compose files to run it either in a production-like configuration (using a copy of the production settings without HTTPS) or in development mode, where it will mount the source code directory as a read-only folder so changes are picked up immediately by the development webserver.

To run in production mode issue the following command:

`docker-compose -f docker-compose.yml up`


The `docker-compose.yml` file has to be passed explicitly because otherwise *docker-compose* will automatically load the `docker-compose.override.yml` file which sets up the containers for development.

To run in development mode simply run this command:

`docker-compose up`

It is also possible to run the development server without Docker by following these steps:

1.  Create a virtual environment, e.g. `python -m venv ~/.venvs/meron_api`
2.  Activate the environment: `source ~/.venvs/meron_api`
3.  Install the development dependencies: `pip install -r meron_api/requirements/development.txt`
4.  Start the development server: `python manage.py runserver`

To access the locally running copy of the API, you can use `localhost:8000` in development mode.
In production mode, it is necessary to add an entry to your `hosts` file that resolves a domain to the IP Docker uses: `172.33.0.2       meron.localdomain`.
Now you can access the API running on your local computer under: [http://meron.localdomain](http://meron.localdomain).
