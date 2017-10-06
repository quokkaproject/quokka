FROM python:3-jessie
MAINTAINER Eric Ho <dho.eric@gmail.com>

ENV FLIT_ROOT_INSTALL 1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install \
	flit \
	pypandoc \
	pygments

RUN apt-get update && \
	apt-get install -y \
		pandoc && \
	rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app/
RUN flit install -s

WORKDIR /work
EXPOSE 5000
ENTRYPOINT ["quokka"]
CMD ["runserver","--host","0.0.0.0","--port","5000"]
