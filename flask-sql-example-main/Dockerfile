FROM python:3.12.3

WORKDIR /src

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "src", "run","--debug", "--host=0.0.0.0"]