import random
import sys
import requests

AWS_URL = "http://mlzmcmp-bike-rental-env.eba-wixby7us.eu-west-1.elasticbeanstalk.com"
LOCAL_URL = "http://localhost:9911"


TEST_RECORDS = [
    # a usual day on early spring
    {
        "season": "spring",
        "mnth": 3,
        "hr": 9,
        "holiday": 0,
        "weekday": "tuesday",
        "workingday": 1,
        "weathersit": 2,
        "temp": 12,
        "atemp": 12,
        "hum": 40,
        "windspeed": 20,
    },
    # afternoon of a warm , late spring day without work
    {
        "season": "spring",
        "mnth": 5,
        "hr": 16,
        "holiday": 1,
        "weekday": "monday",
        "workingday": 0,
        "weathersit": 1,
        "temp": 20,
        "atemp": 20,
        "hum": 30,
        "windspeed": 15,
    },
    # a stormy summer day
    {
        "season": "summer",
        "mnth": 7,
        "hr": 9,
        "holiday": 0,
        "weekday": "wednesday",
        "workingday": 1,
        "weathersit": 4,
        "temp": 11,
        "atemp": 7,
        "hum": 61,
        "windspeed": 49,
    },
    # a hot summer day at noon
    {
        "season": "summer",
        "mnth": 8,
        "hr": 12,
        "holiday": 0,
        "weekday": "thursday",
        "workingday": 1,
        "weathersit": 1,
        "temp": 31,
        "atemp": 35,
        "hum": 11,
        "windspeed": 4,
    },
    # a hot summer day in the afternoon
    {
        "season": "summer",
        "mnth": 8,
        "hr": 16,
        "holiday": 0,
        "weekday": "friday",
        "workingday": 1,
        "weathersit": 1,
        "temp": 31,
        "atemp": 35,
        "hum": 11,
        "windspeed": 4,
    },
    # a hot summer day in the evening
    {
        "season": "summer",
        "mnth": 8,
        "hr": 21,
        "holiday": 0,
        "weekday": "tuesday",
        "workingday": 1,
        "weathersit": 1,
        "temp": 31,
        "atemp": 35,
        "hum": 11,
        "windspeed": 4,
    },
    # weekend in the indian summer
    {
        "season": "fall",
        "mnth": 9,
        "hr": 19,
        "holiday": 0,
        "weekday": "saturday",
        "workingday": 0,
        "weathersit": 1,
        "temp": 24,
        "atemp": 26,
        "hum": 33,
        "windspeed": 12,
    },
    # morning of a cloudy day in the fall
    {
        "season": "fall",
        "mnth": 10,
        "hr": 6,
        "holiday": 0,
        "weekday": "saturday",
        "workingday": 0,
        "weathersit": 2,
        "temp": 13,
        "atemp": 9,
        "hum": 40,
        "windspeed": 23,
    },
    # a cold winter day
    {
        "season": "winter",
        "mnth": 12,
        "hr": 7,
        "holiday": 0,
        "weekday": "friday",
        "workingday": 1,
        "weathersit": 3,
        "temp": 3,
        "atemp": 0,
        "hum": 22,
        "windspeed": 19,
    },
]


def is_aws_app_available():
    awsresp = requests.get(AWS_URL)
    if awsresp.status_code == 200:
        return True
    else:
        return False


def get_prediction(data, url):
    presp = requests.post(f"{url}/predict", json=data)
    presp.raise_for_status()
    rj = presp.json()
    return rj["predicted_rentals_cnt"]


if __name__ == "__main__":

    if is_aws_app_available():
        url = AWS_URL
    else:
        url = LOCAL_URL

    # server URL can be given as input param (e.g. when different port as 9911 is used)
    if len(sys.argv) > 1:
        url = sys.argv[1]

    print(f"Running a test for Bike Rental Prediction using {url} as server....")

    test_data = random.choice(TEST_RECORDS)

    print(
        f"Predicting bike usage for the following input parameters:\n{test_data}\n...."
    )

    prediction = get_prediction(data=test_data, url=url)

    print(
        f"The predicted number of rented bikes is: {prediction}\nThanks for using the service und Tschüss!"
    )
