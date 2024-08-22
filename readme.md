


# Get public and private keys in Synology NAS
To obtain the public and private keys:
```bash
ssh-keygen -t rsa
chmod 600 ~/.ssh/id_rsa
```
Now you can copy the id_rsa content and paste it in Github.

# Install
To clone and install the application:
```bash
git clone git@github.com:jmcordoba/synology_flask.git
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

# Update
To update the application:
```bash
git pull
source .venv/bin/activate
pip3 install -r requirements.txt
```

# PyLint
To get a report of the quality of one python script:
```bash
pylint app.py
```
To get a report of the quality of all the python scripts of a concrete directory:
```bash
find . -type f -name "*.py" | xargs pylint 
```

# Test
To run tests by executing the following command inside the container:
* All tests:
```bash
python3 -m unittest discover -v
```
* Specific test:
```bash
python3 -m unittest test/test_infra/test_shared.py
```

# Start in local host
To start the flask server in local host with IP 0.0.0.0 (localhost) and port 80:
```bash
flask run --host=0.0.0.0 --port=80
```

# Docker commands

## Start commands
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

## Stop commands
To stop the execution of the container
```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)
docker image prune -a --force
```

## Info
To get information of the running containers:
```bash
docker ps -a
```
To get information of the downloaded images:
```bash
docker images
```
