FROM node:18.18.0-bullseye-slim AS base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3

# Set up app dir
WORKDIR /app/

COPY app.js package*.json setup-challenge.py /app/
RUN mkdir public views
COPY ./public/* public
COPY ./views/* views

# Now create the special /challenge directory
RUN mkdir /challenge && \
    chmod 700 /challenge

FROM base AS challenge
# Bring in FLAG from cmgr. Busts the cache every time.
ARG FLAG

# Install latest node packages
RUN npm install

# Create challenge metadata
RUN python3 setup-challenge.py && \
    rm setup-challenge.py

# Create artifacts needed
RUN tar czvf /challenge/artifacts.tar.gz app.js

EXPOSE 3000
# PUBLISH 3000 AS web

CMD ["node", "app.js"]
