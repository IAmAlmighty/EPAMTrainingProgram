FROM jenkins/jenkins

USER root

RUN apt-get update
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y python3.11
RUN apt-get install -y python3-pip
RUN apt-get install -y python3.11-venv
RUN python3 -m venv venv
RUN . /venv/bin/activate

USER jenkins