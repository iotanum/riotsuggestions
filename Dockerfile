FROM python:3.6

ARG discord_api
ARG command_prefix
WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./launcher.py" ]
