FROM python:latest
WORKDIR /usr/app/src

# Copy your application code
COPY ./python/Improviser.py ./
COPY ./python/Pathcounter.py ./
COPY ./python/Example.py ./
COPY ./grid.csv ./

# Copy the requirements file into the image
COPY ./requirements.txt .

# Update the package list and install nano
RUN apt-get update && apt-get install -y nano

# Install the packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt