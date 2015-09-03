FROM alpine
MAINTAINER Bruno Rocha <rochacbruno@gmail.com>
WORKDIR /tmp
COPY requirements/requirements.txt /tmp/
COPY requirements/test.txt /tmp/
COPY requirements/dev.txt /tmp/
RUN apk update
RUN apk add gcc python py-pip libjpeg zlib zlib-dev tiff freetype git py-pillow python-dev musl-dev bash
RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/test.txt
RUN pip install -r /tmp/dev.txt

# docker run --link <mongo_container_id>:mongo -v $PWD:/quokka -t -i quokka/quokkadev /bin/bash
