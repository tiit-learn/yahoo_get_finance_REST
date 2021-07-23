FROM python:3.9

EXPOSE 5000

RUN python3 -m venv venv

COPY requirements.txt requirements.txt
RUN /venv/bin/pip install -r requirements.txt

ADD app.py .
ADD templates /templates
CMD ["/venv/bin/python3", "app.py"]
