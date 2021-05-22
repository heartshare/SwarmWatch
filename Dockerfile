FROM python:3.9.4-alpine3.13

WORKDIR /usr/local/SwarmWatch

COPY . .

RUN pip install -e .

CMD [ "python", "-m", "SwarmWatch.main" ]