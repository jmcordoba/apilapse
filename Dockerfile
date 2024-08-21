#FROM python:3.12-alpine
#COPY app/. .
#RUN pip install -r requirements.txt
#CMD ["python", "app.py"]

# Use an official Python runtime as a parent image
FROM python:3 
ENV FLASK_ENV=production
# Set the working directory in the container
WORKDIR /app
COPY app/. .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD flask run --host=0.0.0.0