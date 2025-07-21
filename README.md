# FastAPIWebApplication

Description
----------------
This exercise aims to develop a comprehensive understanding of building modern web applications using FastAPI, an efficient and fast framework for building APIs in Python. You will create a two-tier application: one service as a backend API and another as a frontend server utilizing Jinja2 templates for dynamic content rendering. This setup provides hands-on experience with FastAPI's powerful features for asynchronous programming, dependency injection, and automatic API documentation, along with integrating front-end technologies for a full-stack development experience. At the same time you will develop a gitlab-ci pipeline that will allow you to have a ci/cd component in your project.

Project Structure Overview:

Backend API Service: Develop a RESTful API service with FastAPI that handles business logic and data management. This service will expose endpoints for CRUD operations on resources (e.g., users, products, or posts).

Frontend Server: Implement a FastAPI application that serves HTML pages, utilizing Jinja2 templates for rendering dynamic content. This server will consume the Backend API for data, providing a user-friendly interface.

gitlab-ci : GitLab CI/CD (Continuous Integration/Continuous Deployment) is a crucial aspect of modern software development, enabling teams to streamline and automate their code integration and deployment processes. GitLab CI/CD is a part of the GitLab platform, an all-in-one DevOps tool that provides an integrated environment for version control, issue tracking, code review, and more. The CI/CD component specifically focuses on automating the building, testing, and deployment of code changes, ensuring that software projects maintain high quality and are released efficiently.

Configuration and Setup Guide:

Project Setup: Create separate directories for the backend and frontend services within your project folder. Initialize a Python virtual environment in each and install FastAPI and Uvicorn (ASGI server).

Backend API Development:

Define your data models using Pydantic for input validation and serialization.

Implement API routes handling CRUD operations, leveraging FastAPI's path operation decorators (e.g., @app.get, @app.post).

Use asynchronous database libraries (e.g., databases with async SQL Alchemy) for non-blocking database operations.

Frontend Server Development:

In the frontend service, set up Jinja2 templates in a templates directory.

Create FastAPI endpoints that render these templates, passing data obtained from the backend API.

Utilize FastAPI's HTTPClient or any async HTTP client library to call the backend API from the frontend service.

Docker-Compose Setup: Define both services in a docker-compose.yml file for easy deployment and local development. Ensure both services are on the same network for internal communication. → https://hfmarkets.atlassian.net/wiki/spaces/DT/pages/42598504/Gitlab+CI+CD 

gitlab-ci: In the context of GitLab, a CI/CD definition refers to the configuration file that outlines the steps, rules, and actions to be taken during the CI/CD pipeline. This definition is usually stored in the project's repository and is written in a YAML format. The definition file, often named '.gitlab-ci.yml', specifies the various stages of the pipeline, such as 'build', 'test', 'deploy', and more. It also includes details about the environment, dependencies, scripts, and rules that govern the pipeline's behavior. By defining the CI/CD pipeline within this file, we can automate tasks like compiling code, running tests, and deploying applications to different environments, leading to improved collaboration, code quality, and faster software delivery. Some examples can be found here: https://docs.gitlab.com/ee/ci/examples/

Docker-Compose Sample:

version: '3'
services:
  backend-api:
    build: ./backend
    command: uvicorn main:app --host 0.0.0.0 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    networks:
      - fastapi-network

  frontend-server:
    build: ./frontend
    command: uvicorn main:app --host 0.0.0.0 --reload
    volumes:
      - ./frontend:/app
    ports:
      - "8080:8000"
    networks:
      - fastapi-network
    depends_on:
      - backend-api

networks:
  fastapi-network:
    external: True


create your network : docker network create fastapi-network --driver=bridge --subnet=192.168.0.1/24

Below is a sample .gitlab-ci.yml file tailored to a FastAPI project. This pipeline configuration leverages Docker and assumes that you have Docker Compose configurations ready for deploying your application.

stages:
  - build
  - test
  - deploy

variables:
  DOCKER_COMPOSE_VERSION: '1.29.2'
  IMAGE_TAG: $CI_REGISTRY_IMAGE/$CI_PROJECT_NAME:$CI_COMMIT_SHORT_SHA

before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

Build Image:
  stage: build
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
  tags:
    - docker

Test:
  stage: test
script:
    - |
      if curl -s --head http://$FASTAPI_HOST:$FASTAPI_PORT/ | grep "200 OK" > /dev/null; then
        echo "The FastAPI application on port $FASTAPI_PORT is up and running."
      else
        echo "The FastAPI application on port $FASTAPI_PORT is not responding."
        exit 1
      fi
  variables:
    FASTAPI_HOST: "localhost"
    FASTAPI_PORT: "8000"
  only:
    - main
  tags:
    - docker

Deploy:
  stage: deploy
  image: docker/compose:$DOCKER_COMPOSE_VERSION
  script:
    - docker pull $IMAGE_TAG
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
  tags:
    - docker

You can use this check_port.py script below for testing as well, or make your own bash script that will not require the socket python package as it is in the gitlab ci file.

import socket

def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout to ensure the check is quick
    result = sock.connect_ex((host, port))
    sock.close()
    
    return result == 0

HOST = "localhost"
PORT = 8000

if check_port(HOST, PORT):
    print(f"The FastAPI application on port {PORT} is up and running.")
else:
    print(f"The FastAPI application on port {PORT} is not responding.")


Explanations for the gitlab-ci configuration:

Stage: The job is placed in a test stage which runs after build and deploy stages. Ensure your stages are defined in the order you want them to execute.

Image: This job uses the curlimages/curl Docker image which is a lightweight image containing the curl command.

Script: The script section attempts to make an HTTP head request to your FastAPI application. If it receives a response with "200 OK", the script reports success. Otherwise, it exits with an error, causing the job, and potentially the pipeline, to fail. Adjust the http://$FASTAPI_HOST:$FASTAPI_PORT/ URL to match where your FastAPI application is deployed.

Variables: FASTAPI_HOST and FASTAPI_PORT are defined in the variables section. Adjust these values based on your deployment details. You might want to pass these variables through CI/CD pipeline settings in GitLab for more flexibility or security.

Only: This job runs only for the main branch. Adjust according to your branch strategy or remove this condition to run on every push to any branch.

Overall Learning Objectives:

Backend API: Understand the principles of RESTful API design, asynchronous programming in Python, and the efficient handling of concurrent requests in web applications.

Frontend Server: Gain experience in web front-end development using template engines, and learn how to integrate a front-end with a RESTful backend service.

Docker and Docker Compose: Enhance your knowledge of containerization, learning how to encapsulate your application's environment for easy development, testing, and deployment.

gitlab-ci: Provide a solid foundation in GitLab CI/CD, equipping you with the skills and knowledge to implement efficient, secure, and automated CI/CD pipelines that support the rapid development and deployment of software applications.

This setup needs also the application files. Here is a guide to make a project in our gitlab and add the files needed per project:

1. Create the Repository on GitLab.hfmarkets.com

Navigate to GitLab: Go to gitlab.hfmarkets.com and log in with your credentials.

Access the DevOps Group: Find and click on the devops group within our organization's GitLab instance.

Create a New Project: Click the "New project" button.

Project Name: Give your project a meaningful name that reflects its purpose.

Visibility Level: Choose "Private" to ensure the project is only accessible to team members unless instructed otherwise.

Initialize with a README: Check this option to automatically create a README.md file in your repository. This is useful for providing an overview or documentation of your project.

2. Clone the Repository Locally

After creating your project, clone it to your local machine using the provided Git command. For example:

git clone https://gitlab.hfmarkets.com/devops/your-project-name.git

Navigate into your project directory:

cd your-project-name

3. Structure Your Project

Ensure your project directory includes the following elements:

Backend Service:

Create a backend directory to contain your backend service code and Dockerfile.

Ensure the backend directory includes:

Application code and dependencies (requirements.txt for Python applications).

A Dockerfile specifying the build instructions for your backend service.

Frontend Service:

Create a frontend directory for your frontend service code and Dockerfile.

The frontend directory should include:

Your static files, HTML templates, and any other resources required by your frontend service.

A Dockerfile to build your frontend service.

Docker Compose File:

At the root of your repository, add a docker-compose.yml file that defines the services, networks, and volumes for your application, following the structure and examples provided earlier.

.gitlab-ci.yml File:

Also at the root, include a .gitlab-ci.yml file to define your CI/CD pipeline according to the learning objectives. This file should instruct GitLab CI/CD on how to build, test, and deploy your services.

4. Push Your Changes

After setting up your project structure and adding the necessary files, commit your changes:

git add .
git commit -m "Initial project setup with backend and frontend services"

Push your changes to the GitLab repository:

git push -u origin main

5. Verify CI/CD Pipeline

Once your changes are pushed, go to your project on gitlab.hfmarkets.com and navigate to the CI/CD section to ensure that your pipeline runs successfully.
