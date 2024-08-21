


# Get public and private keys in Synology NAS

```bash
ssh-keygen -t rsa
chmod 600 ~/.ssh/id_rsa
```
Now you can copy the id_rsa content and paste it in Github

# Install

```bash
git clone git@github.com:jmcordoba/synology_flask.git
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

# Update

```bash
git pull
source .venv/bin/activate
pip3 install -r requirements.txt
```

# PyLint
Execute the following command to get a report of the quality of one python script:
```bash
pylint app.py
```
Execute the following command to get a report of the quality of all the python scripts of a concrete directory:
```bash
find . -type f -name "*.py" | xargs pylint 
```

# Test
You can run tests by executing the following command inside the container:
* All tests:
```bash
python3 -m unittest discover -v
```
* Specific test:
```bash
python3 -m unittest test/test_infra/test_shared.py
```

# Docker commands

## Start commands
```bash
docker build -t webpy .
docker run -p 80:8080 webpy # from localhost:80 to container:8080


docker-compose up
docker-compose up -d
docker exec -ti uwsgi-nginx-flask-python-sqlite-docker-example-web-1 /bin/bash
docker stop 3fd08745f515
```

## Stop commands
```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)
docker image prune -a --force
```

## Info
Containers running:
```bash
docker ps -a
```
Downloaded images:
```bash
docker images
```
