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
    "secret_key": "your-secret-key",
    "email_enabled": false
}
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
cd app
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

## Update
To update the application:
```bash
git pull
source .venv/bin/activate
cd app
pip install --upgrade pip
pip3 install -r requirements.txt
```

## Start in local host
To start the flask server in local host with IP 0.0.0.0 (localhost) and port 80:
```bash
flask run --host=0.0.0.0 --port=80
```
To start the flask server executing the main python script:
```bash
cd app
python3 app.py
```
