# apilapse

## Needed files

You need to create the following file:

```bash
app/conf/dev.json
```

and type the following content:

```json
{
    "host": "localhost",
    "port": 8080,
    "debug": true,
    "database_name": "db/apilapse.db",
    "email": "apilapse@gmail.com",
    "email_password": "dqxmsbvmszutksmi",
    "secret_key": "your-secret-key"
}
```

## Frontend

### Requirements

Ensure that npm (Node Package Manager) and Node.js are both installed on your PC. If not, you can download and install them from https://nodejs.org, which is the official website.

This app has been tested in node 23.4.0 and npm 10.9.2

### To create a react application

```bash
npm install -g create-react-app
npx create-react-app frontapp
```

### To start the front app

```bash
npm start
```

## Backend

### Get public and private keys in Synology NAS
To obtain the public and private keys:
```bash
ssh-keygen -t rsa
chmod 600 ~/.ssh/id_rsa
```
Now you can copy the id_rsa content and paste it in Github.

### Install
To clone and install the application:
```bash
git clone git@github.com:jmcordoba/apilapse.git
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
cd app
pip3 install -r requirements.txt
```

## Update
To update the application:
```bash
git pull
source .venv/bin/activate
cd app
pip3 install -r requirements.txt
```

## PyLint
To get a report of the quality of one python script:
```bash
pylint app.py
```
To get a report of the quality of all the python scripts of a concrete directory:
```bash
find . -type f -name "*.py" | xargs pylint 
```

## Test
To run tests by executing the following command inside the container:
* All tests:
```bash
python3 -m unittest discover -v
```
* Specific test:
```bash
python3 -m unittest test/test_infra/test_shared.py
```

## Start in local host
To start the flask server in local host with IP 0.0.0.0 (localhost) and port 80:
```bash
flask run --host=0.0.0.0 --port=80
```
To start the flask server executing the main python script:
```bash
python3 app.py
```

## Docker commands

### Start commands
Start just with Dockerfile:
```bash
docker build -t webpy .
docker run -p 80:8080 webpy # from localhost:80 to container:8080
```
Start with docker compose:
```bash
docker-compose up
docker-compose up -d
```
To go inside the container:
```bash
docker ps -a
docker exec -ti uwsgi-nginx-flask-python-sqlite-docker-example-web-1 /bin/bash
```

### Stop commands
To stop the execution of the container
```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)
docker image prune -a --force
```

### Info
To get information of the running containers:
```bash
docker ps -a
```
To get information of the downloaded images:
```bash
docker images
```
