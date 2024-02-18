# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

# start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]