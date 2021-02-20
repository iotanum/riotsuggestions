FROM python:3.6

ENV discord_api=${discord_api}
ENV command_prefix=${discord_api}
WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./launcher.py" ]
