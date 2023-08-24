FROM python:3

WORKDIR /usr/src/app

COPY Pipfile ./
RUN pip install pipenv
RUN pipenv install

COPY . .

CMD [ "python", "./main.py" ]
