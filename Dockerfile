FROM python:3.6

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
