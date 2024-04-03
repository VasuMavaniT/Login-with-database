# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Set environment variables for Postgres
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=admin

# Install required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip postgresql && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source /venv/bin/activate

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Expose PostgreSQL port
EXPOSE 5432

# Start PostgreSQL service
RUN service postgresql start

# Create PostgreSQL database and user with necessary rights
USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE DATABASE $POSTGRES_DB;" &&\
    psql --command "ALTER USER $POSTGRES_USER WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';" &&\
    psql --command "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"

# Run the python file database.py
RUN python3 database.py

# Expose the port on which the Python application will run
EXPOSE 8097

# Start the Python application
CMD ["/venv/bin/python", "app.py"]
