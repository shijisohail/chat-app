# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8008 available to the world outside this container
EXPOSE 80

# Define the command to run your application with Daphne
#CMD daphne -b 0.0.0.0 -p 80 channels_sockets.asgi:application
