FROM python:3.8.7-buster

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libc-dev \
    netcat \
    ; \
    rm -rf /var/lib/apt/lists/*

RUN pip install numpy==1.19.4
RUN pip install pandas==1.1.4
RUN pip install psycopg2==2.8.6
RUN pip install psycopg2-binary==2.8.6
RUN pip install matplotlib==3.3.3
RUN pip install scikit-learn==0.23.2
RUN pip install Keras==2.4.3
RUN pip install jupyter==1.0.0

RUN pip install Cython>=0.22 \
    cmdstanpy==0.9.5 \
    LunarCalendar>=0.0.9 \
    convertdate>=2.1.2 \
    holidays>=0.10.2 \
    setuptools-git>=1.2 \
    python-dateutil>=2.8.0 \
    tqdm>=4.36.1

RUN pip install pystan==2.19.1.1
RUN pip install fbprophet==0.7.1

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY src docker-entrypoint.sh /app/

WORKDIR /app

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]