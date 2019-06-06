# This Dockerfile uses Docker Multi-Stage Builds
# See https://docs.docker.com/engine/userguide/eng-image/multistage-build/
# Requires Docker v17.05

# Base image for build and runtime
FROM python:3.8.0a4-stretch AS base
LABEL maintainer="Eric Ho <dho.eric@gmail.com>"

WORKDIR /usr/src/app
ENV DEBIAN_FRONTEND=noninteractive \
    PBR_VERSION=4.2.0

# Build image
FROM base AS build

# Install build packages
RUN apt-get update && apt-get install -yq --no-install-recommends \
            pandoc \
            build-essential \
            python3-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN pip install \
        pypandoc \
        pygments \
        pbr==${PBR_VERSION}

# Copy app
COPY . /usr/src/app/

# Generate docs
RUN pandoc --from=markdown --to=rst --output=README.rst README.md

# Install app
RUN python setup.py develop

# Runtime image
FROM base AS run

# Copy from build image
COPY --from=build /usr/src/app/ /usr/src/app/
COPY --from=build /usr/local/lib/python3.8/ /usr/local/lib/python3.8/
COPY --from=build /usr/local/bin/quokka /usr/local/bin/quokka

WORKDIR /usr/src/app/quokka/project_template

# Setup admin user
# Default user and password: admin/admin
RUN quokka adduser --username admin --password admin --fullname admin --email 'admin@localhost'

EXPOSE 5000

ENTRYPOINT ["quokka"]
CMD [ "runserver", "--host", "0.0.0.0", "--port", "5000" ]
