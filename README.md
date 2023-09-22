# Overview

You can set the required parameters by creating an `.env` file in the service directory. To find out what parameters the service needs, you can look at the `core\config.py` file.

### Install Libraries
    pip3 install -r requirements.txt


### The Microservice backend api, uses the REST API interface to accept request from the frontend part of the project

### Run service
    uvicorn app:app --reload

### Documentation available on
    http://localhost:8000/docs

### Run & Build containers
    docker-compose up --build -d

### Stop containers
    docker-compose down
