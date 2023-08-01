# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY ./docker/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt


# Make port 6000 available to the world outside this container
EXPOSE 6000

# Define environment variable
ENV PYTHONPATH /app

# Run server.py when the container launches
CMD ["python", "./server/server.py"]
