find . -type f -name "*.py" | grep -v ".venv" | grep -v "app/test/" | xargs pylint --fail-under=9