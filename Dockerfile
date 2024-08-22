FROM python:3.12-alpine
# the following content will be available inside the container
ENV FLASK_ENV=production
# defining the name of the directory to place the application
WORKDIR /project
# copy the content of the app in the working directory
COPY app/. .
# install the dependencies of the application
RUN pip install -r requirements.txt
#RUN apk update
#RUN apk add git
#RUN git config --global user.name "Your Name"
#RUN git config --global user.email "your.email@example.com"
#RUN pylint $(git ls-files '*.py')
RUN pylint app.py
RUN find src/. -type f -name "*.py" | xargs pylint
RUN find test/. -type f -name "*.py" | xargs pylint
# expose the port 8080
EXPOSE 8080
# 
#CMD ["python", "app.py"]
CMD flask run --host=0.0.0.0 --port=8080