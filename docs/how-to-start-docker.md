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
