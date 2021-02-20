FROM python:3.6

ARG DISCORD_API
ARG COMMAND_PREFIX
ENV DISCORD_API $DISCORD_API
ENV COMMAND_PREFIX $COMMAND_PREFIX

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./launcher.py" ]
