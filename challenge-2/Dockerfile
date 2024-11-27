FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set up app dir
WORKDIR /app/

COPY manage.py setup-challenge.py requirements.txt setup.sh /app/
RUN mkdir /app/app /app/webapp
COPY app/. /app/app/
COPY webapp/. /app/webapp/

RUN python3 -m pip install -r requirements.txt

# Now create the special /challenge directory
RUN mkdir /challenge && \
    chmod 700 /challenge

FROM base AS challenge
# Bring in FLAG from cmgr. Busts the cache every time.
ARG FLAG

# Create challenge metadata
RUN python3 setup-challenge.py && \
    rm -f setup-challenge.py

# Set up DB 
RUN chmod +x setup.sh && /app/setup.sh && rm -f /app/setup.sh

# Create artifacts needed
RUN cp /app/app/views.py ./
RUN tar czvf /challenge/artifacts.tar.gz views.py
RUN rm -f views.py 
EXPOSE 8000
# PUBLISH 8000 AS web

CMD ["python3", "/app/manage.py", "runserver", "0.0.0.0:8000"]