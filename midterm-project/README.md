# Machine Learning Zoomcamp Midterm Project
# Predicting bike sharing rentals

This is my submission for the [Machine Learning Zoomcamp's Midterm Project](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/07-midterm-project). 

## Problem statement

I've chosen the [Bike Sharing Dataset](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset#), which contains 2 years of data of the Capital Bikeshare system in
Washington DC. The exact dataset I worked with is preprocessed and enriched by Hadi Fanaee from the University of Porto - I retrieved it from the public
[machine learning data repository of UC Irvine](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset#).

The dataset contains hourly rental data with the following attributes (based on the README provided with the file):

	- instant: record index
	- dteday : date
	- season : season (1:spring, 2:summer, 3:fall, 4:winter) - 
            the app receives both integers and names of the months
	- yr : year (0: 2011, 1:2012)
	- mnth : month ( 1 to 12)
	- hr : hour (0 to 23)
	- holiday : weather the day given by dteday is holiday or not
	- weekday : day of the week 0-6, where 0 is Sunday and 6 is Saturday.  
                the app receives both integers and names of the days
	- workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
	- weathersit : 
		- 1: Clear, Few clouds, Partly cloudy, Partly cloudy
		- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
		- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
		- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
	- temp : Normalized temperature in Celsius. The values are divided to 41 (max)
	- atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
	- hum: Normalized humidity. The values are divided to 100 (max)
	- windspeed: Normalized wind speed. The values are divided to 67 (max)
	- casual: count of casual users
	- registered: count of registered users
	- cnt: count of total rental bikes including both casual and registered

I used all the attributes to build the model, except the followings: `instant`, `yr`, `casual`, `registered`.
I considered the task as a regression problem, where the target is the number of bikes rented in a given hour (variable `cnt` in the dataset). 
My goal during the optimization of the model was to minimize root mean squared error (RMSE).
Sources:
- the description of the data can be found here: [https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset#]()
- the dataset can be downloaded from here: [https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip]()
    - it's a zipped dataset, which contains the followings:
        - `Readme.txt` - details about the dataset
        - `hour.csv` - hourly bike rental data - the one which I actually used
        - `day.csv` - daily aggregated dataset

# Main products

- `notebook.ipynb` - Jupyter notebook containing the data acquisition, the data exploration, data splitting steps and the experiments with different models
- `train.py` 
    - a script-ed version of the data acquisition and model training, including downloading the data, tuning the model and saving the best one
    - it doesn't just train the best model (RandomTreeRegressor) but goes through on all the options from LinearRegression, through Ridge, Lasso and DecisionTreeRegressor
    - at the end, it selects the (or one of the) best model with the lowest RMSE
    - running the script
        1. create and activate pipenv (see section "Installing dependencies and using virtual environment")
        2. `python train.py` runs all the steps. 
           Optionally, you can give the model filename as input param (e.g. `python train.py mypreciousmodel`) you want to save your model. 
           It will be placed in the folder `midterm-project/models`. 

- `predict_bikerental.py`
    - creates and runs a web app on port 9911
        - the app has the following endpoints:
            - `/` (method `GET`) - a simple healthcheck endpoint
            - `/predict` (method `POST`) - predicting the number of bike rentals
    - does basic (not extensive) validation on the input data
    - transforms the data to make it consumable for the model

- `Dockerfile` - in order to build a Docker image of the app, including being able to deploy on AWS Elastic Beanstalk
- `test_api.py`
    - simple script with pre-loaded test data
    - for details see the section "Running the test script" below


# Running and deploying the app

i) Clone/download this repo
ii) For all the below steps, make sure current directory is `midterm-project`

## Installing dependencies and using virtual environment

These steps are necessary to run the prediction app locally and run the test script.

1. Installing dependencies `pipenv install`
2. Entering virtual environment `pipenv shell`

## Running the app locally
In order to run the app, issue `python predict_bikerental.py`. 
The app will be available under `http://localhost:9911/` and `http://localhost:9911/predict` (POST method).

## Building and running the app in a Docker image

1. Build the image using `docker build -t mlzoomcamp-bike-rental:1.0 -f Dockerfile .`
   or you can get it from Dockerhub: `docker pull akosbence/mlzoomcamp-bike-rental:1.0`
2. `docker run -ti -p 9911:9911 mlzoomcamp-bike-rental:1.0` (in case of Dockerhub image use `akosbence/mlzoomcamp-bike-rental:1.0`)
    - if you want to map the service on your machine to a port other than 9911,  use `-p <YOUR_PORT_NUMBER>:9911` instead
3. Similarly to the non-dockerized solution, the app is available under `http://localhost:9911/` and `http://localhost:9911/predict` (POST method).
   
## Deploying to AWS Elastic Beanstalk
The next steps presume that you have EB CLI installed and set up (e.g. auth keys) with the corresponding AWS permissions. 
If that's not the case, follow the [instructions of AWS](
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html).

1. Initializing EB config `eb init -p docker -r eu-west-1 mlzmcmp-bike-rental`
2. (Optional) Check app locally: `eb local run --port 9911` - this spins up the service locally using EB and Docker 
3. Deploying app to AWS: `eb create mlzmcmp-bike-rental-env` - builds and deploys the app, including provisioning all the necessary services. The app can be changed by `eb deploy mlzmcmp-bike-rental-env`.
4. The app is available under `mlzmcmp-bike-rental-env.eba-wixby7us.eu-west-1.elasticbeanstalk.com` (again, the root path gives just a health check status,
while the bike rental prediction service is available under the `/predict` endpoint using POST method).
**Please note that the app will be available on AWS until 15 November 2021 23:59 CET**

# Testing and using the app

## Running the test script
- the module has some pre-built test data, from which one is chosen randomly per run and the app is called using it
- in order to run the test script, issue `python test_api.py`. It will run one of the pre-defined test cases and print
    - by default, it sends the request to the app deployed on AWS EB, if that's not available, it looks for a local deployment
    - you can also supply a URL as input param, e.g. `python test_api.py http://localhost:8989` (no need to add `/predict`)
the most important steps of the process to stdout.
  
## Sending the request manually
- if you want to test the app by using your weapon of choice (e.g. Postman, curl, requests) and or test data, send a POST request to the app
  (e.g. `http://mlzmcmp-bike-rental-env.eba-wixby7us.eu-west-1.elasticbeanstalk.com/predict`) with the following input parameters:
  - `season`, `mnth`, `hr`, `holiday`, `weekday`, `workingday`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`
  - for the descriptions and value ranges please see the problem statement (above)
- sample request body
    `{ "season": "summer", "mnth":6, "hr": 10, "holiday": 0, "weekday":"saturday", "workingday":0,
    "weathersit":1, "temp":28, "atemp": 33, "hum": 9,"windspeed": 5 }`


