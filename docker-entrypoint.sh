#!/bin/sh

set -e

while ! nc -z ${DB_HOST} ${DB_PORT}; do echo "DB not ready" && sleep 1; done;
while ! nc -z ${DB_ANALYTICS_HOST} ${DB_ANALYTICS_PORT}; do echo "ANALYTICS DB not ready" && sleep 1; done;

python api.py