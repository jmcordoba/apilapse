## PyLint
To get a report of the quality of one python script:
```bash
pylint app.py
```
To get a report of the quality of all the python scripts of a concrete directory:
```bash
find . -type f -name "*.py" | xargs pylint 
```

## Unit Test
To run tests by executing the following command inside the container:
* All tests:
```bash
python3 -m unittest discover -v
```
* Specific test:
```bash
python3 -m unittest test/test_infra/test_shared.py
```

## Playwright Test
To run tests by executing the following command inside the container:
* All tests:
```bash
pytest
```
* Specific test:
```bash
pytest tests/test_general.py
```
