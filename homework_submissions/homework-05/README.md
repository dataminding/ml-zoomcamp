# ML Zoomcamp Homework 5 submission 

[Exercises can be found here](https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/05-deployment/homework.md)

### Q1 - Q2
	- I used the CLI and file browser for the solutions 

### Q3
 - solution can be found the Jupyter notebook `homework-05.ipynb`

### Q4
 - the server code can be found the module `churn.py`, the testing using `requests` is contained by the Jupyter notebook (`homework-05.ipynb`)
 - I've downloaded the files `dv.bin` and `model1.bin` to a separate folder called `models-transformers` and loaded them from there (they aren't uploaded to this repo, you can find the references in the Zoomcamp's repo (see above)). That's why `.dockerignore` contains this folder.
 - ran the app using Gunicorn

### Q5
 - solution is in the `Dockerfile`
 - I've pulled the base image before building obtained the image ID the following way:
 	`$ docker images | grep agrigorev/zoomcamp-model | awk '{print $3}'`

### Q6
 - extended the code to work on both on the host machine or on Docker - in order to run the docker version, the environment variable `ENV` should be set to `docker`
 - the app runs on the PORT 9222
 - example for building and using the image:
 ```
$ docker build --tag zoomcamp-hw5:10.10.2021 -f Dockerfile .
$ docker run -e ENV=docker -p 9222:9222 zoomcamp-hw5:10.10.2021
 ```