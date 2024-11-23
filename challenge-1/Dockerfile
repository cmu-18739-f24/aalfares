FROM node:18.18.0-bullseye-slim

# Put your ctf anywhere *but* /challenges. That is special to cmgr. 
WORKDIR /app

# You can copy multiple things at once
COPY app.js package*.json del-funkee.txt ./ 

# mkdir accepts multiple arguments
RUN mkdir public views

COPY ./public/initial.md public/initial.md
COPY ./views/* views


RUN npm install


# Now create the special /challenge directory
RUN mkdir /challenge && \
    chmod 700 /challenge

# Create secret challenge metadata
RUN echo "{\"flag\":\"$(cat del-funkee.txt)\"}" > /challenge/metadata.json

# Create artifacts needed
RUN tar czvf /challenge/artifacts.tar.gz app.js

EXPOSE 3000
# PUBLISH 3000 AS web


CMD ["node", "app.js"]
