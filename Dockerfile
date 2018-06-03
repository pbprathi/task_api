FROM ubuntu:latest

ENV LANG C.UTF-8

CMD ["/bin/bash"]

#RUN export LANG=C.UTF-8

RUN apt-get update && apt-get install -y python3 python3-pip libmysqlclient-dev mysql-client

RUN pip3 install flask Flask-SQLAlchemy mysqlclient

copy app.py /opt/app.py

ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0 --port=5000
