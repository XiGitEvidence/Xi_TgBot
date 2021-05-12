FROM python:2.7

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD main.py main.py

EXPOSE 5000
CMD ["sh","-c","python main.py"]
