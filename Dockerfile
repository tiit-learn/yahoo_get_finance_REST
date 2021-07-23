FROM python:3.9

EXPOSE 4545

RUN python3 -m venv venv

COPY requirements.txt requirements.txt
RUN /venv/bin/pip install -r requirements.txt

ADD app.py .
CMD ["/venv/bin/python3", "app.py"]
