# Machine Learning Zoomcamp Capstone Project
# Fake Job Posting prediction

This is my submission for the [Machine Learning Zoomcamp's Capstone Project](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/12-capstone). 

## Problem statement

As the topic of the Capstone Project, I've chosen the detection of real/fake job postings. The dataset is available on [Kaggle](https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction).
It contains about ~18k records with job postings marked as real or fraudlent. I considered this as a binary classification problem, where the goal was to identify
whether a job posting is real or fake (fraudlent).
The dataset contains following attributes:

    - job_id: a record ID, which isn't considered by the model
	- title: name/title of the job posting (e.g. Bill Review Manager)
    - location: shows where the job is located. geo hierarchies are stored comma separated in this field, 
      so I've splitted it to the following pieces:
        - country (e.g. US)
        - state (e.g. CA)
        - city (e.g. San Francisco)
	- department: dept. within the company (e.g. Sales)
	- salary_range: string field showing the salary in USD (e.g. 20000-28000)
	- company_profile: short description of the company in free text form
	- description: description of the job/position in free text form
	- requirements: requirements to fulfill to get the job, in free text form
	- benefits: benefits related to the job, in free text form
	- telecommuting: binary flag showing if remote work is possible
	- has_company_logo: binary flag showing if a company logo belongs to the posting
	- has_questions: binary flag showing if screeniing questions are available
	- employment_type: full-time, part-time, contract etc.
	- required_experience: experience needed to fulfill the job (e.g. executive)
	- required_education: e.g. Bachelor
	- industry: where the company is present (e.g. Automotive)
	- function: function of the position within the organization (e.g. Research)
    - fraudlent: binary flag showing if the job posting is real or fake. this is the target variable

Since the dataset contains textual data (e.g. `description`), I've preprocessed those columns with `TfIdfVectorizer`. 
The optimization criteria was to achieve the best ROC AUC value.

# Main products

- `capstone-project.ipynb` - Jupyter notebook containing the data exploration + preprocessing steps and experiments with different models 
  (e.g. logistic regression, decision tree) and parameters
- `train.py` 
    - a script-ed version of the data acquisition and model training, including downloading the data, 
      training the best model (chosen in `capstone-project.ipynb`) and saving the model with the transformer into files (`capstone_model.pickle`, `capstone_transformer.pickle`)
    - running the script
        1. create and activate pipenv (see section "Installing dependencies and using virtual environment")
        2. `python train.py <0/1>` runs all the steps. The flag `1` makes the script download the dataset. If the data is already in the folder 
           and is named `fake_job_postings.csv`, use flag `0`.

- `predict_fake_job.py`
    - creates and runs a web app on port 9911
        - the app has the following endpoints:
            - `/` (method `GET`) - a simple healthcheck endpoint
            - `/detect` (method `POST`) - predicting whether a posting is fake or not
    - validates and transforms the input data
    - applies the model on the preprocessed data and emits the prediction

- `Dockerfile` - in order to build a Docker image of the app, including being able to deploy on AWS Elastic Beanstalk
- `test_api.py`
    - simple script with pre-loaded test data
    - for details see the section "Running the test script" below
    
# Getting the dataset
- the description of dataset is available here: https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction
- the dataset can be downloaded from here: https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction/download
- if you don't have a Kaggle account or just want to get it faster, you can use this link instead [https://bit.ly/3pLvxaV]. 


# Running and deploying the app

i) Clone/download this repo
ii) For all the below steps, make sure current directory is `capstone-project`

## Installing dependencies and using virtual environment

These steps are necessary to run the prediction app locally and run the test script.

1. Install dependencies `pipenv install`
    - you might need `pipenv install --pre`
    - if you're having troubles with SciPy installation on Mac OS (especially Big Sur), `export SYSTEM_VERSION_COMPAT=1`
2. Enter virtual environment `pipenv shell`

## Running the app locally
In order to run the app, issue `python predict_fake_job.py`. 
The app will be available under `http://localhost:9911/` (health check) and `http://localhost:9911/detect` (POST method).

## Building and running the app in a Docker image

1. Build the image using `docker build -t mlzoomcamp-fake-job-detector:1.0 -f Dockerfile .`
   or you can get it from Dockerhub: `docker pull akosbence/mlzoomcamp-fake-job-detector:13.12.2021`
2. `docker run -ti -p 9911:9911 mlzoomcamp-fake-job-detector:1.0` (in case of Dockerhub image use `akosbence/mlzoomcamp-fake-job-detector:13.12.2021`)
    - if you want to map the service on your machine to a port other than 9911,  use `-p <YOUR_PORT_NUMBER>:9911` instead
3. Similarly to the non-dockerized solution, the app is available under `http://localhost:9911/` and `http://localhost:9911/detect` (POST method).
   
## Deploying to AWS Elastic Beanstalk
The next steps presume that you have EB CLI installed and set up (e.g. auth keys) with the corresponding AWS permissions. 
If that's not the case, follow the [instructions of AWS](
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html).

1. Initializing EB config `eb init -p docker -r mlzoomcamp-fake-job-detector`
2. (Optional) Check app locally: `eb local run --port 9911` - this spins up the service locally using EB and Docker 
3. Deploying app to AWS: `eb create mlzoomcamp-fake-job-detector-env` - builds and deploys the app, including provisioning all the necessary services. The app can be changed by `eb deploy mlzmcmp-bike-rental-env`.
4. The app is available under `http://mlzoomcamp-fake-job-detector-dev.eu-west-1.elasticbeanstalk.com` (again, the root path gives just a health check status,
while the bike rental prediction service is available under the `/detect` endpoint using POST method).
**Please note that the app will be available on AWS until 21 December 2021 23:59 CET**

# Testing and using the app

## Running the test script
- the module has some pre-built test data, from which one is chosen randomly per run and the app is called using it
- in order to run the test script, issue `python test_api.py`. It will run one of the pre-defined test cases and print
    - by default, it sends the request to the app deployed on AWS EB, if that's not available, it looks for a local deployment
    - you can also supply a URL as input param, e.g. `python test_api.py http://localhost:8989` (no need to add `/detect`)
the most important steps of the process to stdout.
  
## Sending the request manually
- if you want to test the app by using your weapon of choice (e.g. Postman, curl, requests) and or test data, send a POST request to the app
  (e.g. `http://mlzoomcamp-fake-job-detector-dev.eu-west-1.elasticbeanstalk.com/detect`) with the following input parameters:
  - `title` , ` department` , ` salary_range` , ` company_profile` , ` description` , ` requirements` , ` benefits` , 
    ` telecommuting` , ` has_company_logo` , ` has_questions` , ` employment_type` , ` required_experience` , 
    ` required_education` , ` industry` , ` function` , ` country` , ` state` , ` city` 
    - if one of parameters is missing, the app will substitute it with default values
  - for the descriptions and value ranges please see the problem statement (above)
- sample request body
    `{"title": "Software Engineer - ASP.NET", "department": null, "salary_range": null, 
  "company_profile": "Enozom is a leading software development company, offering custom software development, software products, offshore software development, professional outsourcing and software consultancy", 
  "description": "ResponsibilitiesThe right candidate will work with system analysts to determine business requirements, prepares technical design forms and builds new software through existing or newly developed codes.Build systems with .NET 4.0 / #URL_01a736d89d2f0b19de700923d2c312837e180465650804d0f84105352812bf9a# / SQL Server \\u00a0/ MVCDevelop new functionality on our existing software products.QualificationsEducation: Bachelor Degree preferably Computer Engineering.Experience: 2+ years in the same field.SkillsAbility to quickly learn new concepts and software is necessary.Deep knowledge of the .NET 3.5/4.0 Framework, including Visual Studio 2008, VB.NET, #URL_01a736d89d2f0b19de700923d2c312837e180465650804d0f84105352812bf9a#.ASMX and WCF Web Services, and #URL_de16367b05c5ad8d662bcb494e7f33613767a6a8881ee57a6328b09d250602b9#.Strong knowledge of software implementation best practices.Strong experience designing and working with n-tier architectures (UI, Business Logic Layer Data Access Layer) along with some experience with service-oriented architectures (SOA).Ability to design and optimise SQL Server 2008 stored procedures.Experience with JQuery or similar technologies.Hand coded XML, XHTML and CSS.", 
  "requirements": null, "benefits": null, "telecommuting": 0, "has_company_logo": 1, "has_questions": 0, 
  "employment_type": null, "required_experience": null, "required_education": null, "industry": null, 
  "function": null, "country": "EG", "state": "ALX", "city": " Alexandria"}`





