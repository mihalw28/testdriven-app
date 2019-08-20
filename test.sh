#!/bin/bash

fails=""

inspect() {
    if [ $1 -ne 0 ]; then
    fails="${fails} $2"
    fi
}

# run unit and integration tests
docker-compose up -d --build
docker-compose exec users python manage.py test
inspect $? users
docker-compose exec users flake8 project
inspect $? users-lint
docker-compose exec client npm run coverage
instpec $? client
docker-compose down

# return proper code
if [ -n "${fails}" ]; then
    echo "Test failed: ${fails}"
    exit 1
else
    echo "Test passed!"
    exit 0
fi