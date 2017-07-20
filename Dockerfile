FROM python:3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client mysql-client python-dev libev-dev\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

WORKDIR /usr/src/app/osqprocessor
CMD ["/usr/local/bin/python3", "./osqprocessor.py"]
