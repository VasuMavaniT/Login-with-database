# Use an official Python image. Choose a version that suits your application.
FROM python:3.8-slim

# Set an environment variable to make Python not buffer stdout and stderr (this is useful for logging)
ENV PYTHONUNBUFFERED=1

# Install system dependencies including libpq-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev  && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8097

# Set environment variables used by the flask command
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the application using the flask run command
CMD ["flask", "run", "--port=8097"]
