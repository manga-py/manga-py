FROM python:3.5

# Where manga will be downloader
VOLUME /data

# Install app
WORKDIR /usr/src/app
COPY . .
RUN pip install -q -r requirements.txt && \
    python setup.py -q install

# Switch back to /data directory
WORKDIR /data

# Define manga-py as entrypoint
ENTRYPOINT ["manga-py"]
