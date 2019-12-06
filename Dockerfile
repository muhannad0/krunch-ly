FROM python:3.7-slim

RUN useradd --create-home --shell /bin/bash krunchly

WORKDIR /home/krunchly

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY krunchly.py config.py setup.sh ./
RUN chmod +x setup.sh

ENV FLASK_APP krunchly.py

RUN chown -R krunchly:krunchly ./
USER krunchly

EXPOSE 5000
ENTRYPOINT ["./setup.sh"]