


# Get public and private keys in Synology NAS

```
ssh-keygen -t rsa
chmod 600 ~/.ssh/id_rsa
```
Now you can copy the id_rsa content and paste it in Github

# Install

```
git clone git@github.com:jmcordoba/synology_flask.git
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

# Update

```
git pull
source .venv/bin/activate
pip3 install -r requirements.txt
```

# PyLint
Execute the following command to get a report of the quality of one python script:
````
pylint app.py
```
Execute the following command to get a report of the quality of all the python scripts of a concrete directory:
````
find . -type f -name "*.py" | xargs pylint 
```