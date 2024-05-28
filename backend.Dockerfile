FROM python:3.10

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./backend /app

EXPOSE 5000

ENV FLASK_APP=stocky.py

CMD ["flask", "run", "--host", "0.0.0.0"]