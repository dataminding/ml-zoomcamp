# Machine Learning Zoomcamp Milestone Project
# Predicting bike sharing rentals


## Problem statement




dataset:
- I've chosen the Bike Sharing Dataset()

- what is the problem, how the solution will be used

-it's a regression problem

- hourly data


https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset#


https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip

`train.py`



- 
- accepts model name as optional parameter
- saves the best model under `./models`
use 

# TODO
### 
README.md with
    Description of the problem

  
# Products


-----------------------------------------------------------------------------

# Running the app

For all the below steps, make sure current directory is `milestone-project`

## Installing dependencies and using virtual environment

These steps are necessary to run the prediction app locally and run the test script.

1. Installing dependencies `pipenv install`
2. Entering virtual environment `pipenv shell`

## Running the prediction app locally
In order to run the app, issue `python predict_bikerental.py`. 
The app will be available on `http://localhost:9911/predict`.

## Running the test script
In order to run the test script, issue `python test_api.py`. It will run one of the pre-defined test cases and print
the most important steps of the process to stdout.

## Building and running the app in a Docker image

1. Build the image using `docker build --tag mlzoomcamp-bike-rental:1.0 -f Dockerfile .`
   or you can get it from Dockerhub: `docker pull akosbence/mlzoomcamp-bike-rental:1.0`
2. `docker run -ti -p 9911:9911 mlzoomcamp-bike-rental:1.0` (in case of Dockerhub image use `akosbence/mlzoomcamp-bike-rental:1.0`)
    - if you want to map the service on your machine to a port other than 9911,  use `-p <YOUR_PORT_NUMBER>:9911` instead
   
## Deploying to AWS Elastic Beanstalk
The next steps presume that you have EB CLI installed and set up (e.g. auth keys) If that's not the case, follow the [instructions on AWS doc](
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html).

1. Initializing EB config `eb init -p docker -r eu-west-1 mlzmcmp-bike-rental`
2. (Optional) Check app locally: `eb local run --port 9911` - this spins up the service locally using EB and Docker 
3. Deploying app to AWS: `eb create mlzmcmp-bike-rental-env` - this deploys the app, including provisioning all the necessary services. The app can be changed by `eb deploy mlzmcmp-bike-rental-env` 
4. The app is available under `mlzmcmp-bike-rental-env.eba-wixby7us.eu-west-1.elasticbeanstalk.com`. Please note that the root path gives just a health check status,
while the bike rental prediction service is available under the `/predict` endpoint using POST method.
**Please note that the app will be available on AWS until 15 November 2021 23:59 CET**
