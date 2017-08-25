FROM hypuk/dockerfile:python

ENV DJANGO_SETTINGS_MODULE = intranet.settings

ENV TZ = Asia/Almaty
RUN mkdir /db && mkdir /static && mkdir /photo && mkdir /django_logs

WORKDIR /code/mlm
COPY ./requirements.txt /code/mlm/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/mlm

CMD bash run.sh