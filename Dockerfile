FROM python:3.8.13
USER root

WORKDIR /app

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install discord
RUN pip install git+https://github.com/Pycord-Development/pycord
RUN pip install ffmpeg-python
RUN pip install flask
RUN pip install Gunicorn
RUN pip install PyNaCl
RUN pip install librosa
RUN pip install numpy
RUN pip install pydub
RUN pip install youtube_dl
RUN pip install soundfile

COPY . /app
