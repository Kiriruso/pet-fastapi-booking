#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app app.tasks.celeryconfig:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app app.tasks.celeryconfig:celery flower
fi