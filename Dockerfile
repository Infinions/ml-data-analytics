FROM python:3.7-stretch

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libc-dev \
    netcat \
    ; \
    rm -rf /var/lib/apt/lists/*

RUN pip install Cython>=0.22 \
    cmdstanpy==0.9.5 \
    pystan>=2.14 \
    numpy>=1.15.4 \
    pandas>=1.1.4 \
    matplotlib>=2.0.0 \
    LunarCalendar>=0.0.9 \
    convertdate>=2.1.2 \
    holidays>=0.10.2 \
    setuptools-git>=1.2 \
    python-dateutil>=2.8.0 \
    tqdm>=4.36.1

RUN pip install fbprophet==0.7.1

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY src docker-entrypoint.sh /app/

WORKDIR /app

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]