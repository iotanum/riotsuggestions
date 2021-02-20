FROM python:3.6-slim

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./launcher.py" ]
