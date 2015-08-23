FROM alpine
MAINTAINER Bruno Rocha <rochacbruno@gmail.com>
WORKDIR /tmp
COPY requirements.txt /tmp/
COPY requirements_test.txt /tmp/
COPY requirements_dev.txt /tmp/
RUN apk update
RUN apk add gcc python py-pip libjpeg zlib zlib-dev tiff freetype git py-pillow python-dev musl-dev bash
RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements_test.txt
RUN pip install -r /tmp/requirements_dev.txt

# docker run --link <mongo_container_id>:mongo -v $PWD:/quokka -t -i quokka/quokkadev /bin/bash
