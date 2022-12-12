FROM ubuntu:18.04

ENV TZ "Asia/Shanghai"
ENV LANG "C.UTF-8"

RUN sed -i 's/archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list && \
    echo $TZ > /etc/timezone && \
    apt update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    python3-pip python3-setuptools python3-wheel python3.6 tzdata && \
    ln -s /usr/bin/python3.6 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

RUN mkdir -p /web/logs
WORKDIR /web

ADD requirements.txt /web/requirements.txt
RUN pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

ADD runserver.py /web/runserver.py
ADD forums /web/forums
ADD templates /web/templates
ADD static /web/static
ADD translations /web/translations

CMD ["gunicorn","-b","0.0.0.0:8000","runserver:app"]
