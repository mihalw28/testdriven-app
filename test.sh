#!/bin/bash


type=$1
fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run server-side tests
server () {
  docker-compose up -d --build
  docker-compose exec users python manage.py test
  inspect $? users
  docker-compose exec users flake8 project
  inspect $? users-lint
  docker-compose exec exercises python manage.py test
  inspect $? exercises
  docker-compose exec exercises flake8 project
  inspect $? exercises-lint
  docker-compose down
}

# run client-side tests
client() {
  docker-compose up -d --build
  docker-compose exec client npm run coverage
  inspect $? client
  docker-compose down
}

# run e2e tests
e2e() {
  docker-compose -f docker-compose-stage.yml up -d --build
  docker-compose -f docker-compose-stage.yml exec users python manage.py recreate_db
  ./node_modules/.bin/cypress run --config baseUrl=http://localhost --env REACT_APP_API_GATEWAY_URL=$REACT_APP_API_GATEWAY_URL,LOAD_BALANCER_STAGE_DNS_NAME=http://localhost
  inspect $? e2e
  docker-compose -f docker-compose-stage.yml down
}

# run all tests
all() {
  docker-compose up -d --build
  docker-compose exec users python manage.py test
  inspect $? users
  docker-compose exec users flake8 project
  inspect $? users-lint
  docker-compose exec exercises python manage.py test
  inspect $? exercises
  docker-compose exec exercises flake8 project
  inspect $? exercises-lint
  docker-compose exec client npm run coverage
  inspect $? client
  docker-compose down
  e2e
}

# run appropriate tests
if [[ "${type}" == "server" ]]; then
  echo
  echo "Running server-side tests!"
  echo
  server
elif [[ "${type}" == "client" ]]; then
  echo
  echo "Running client-side tests!"
  echo
  client
elif [[ "${type}" == "e2e" ]]; then
  echo
  echo "Running e2e tests!"
  echo
  e2e
else 
  echo
  echo "Running all tests!"
  echo
  all
fi

# return proper code
if [ -n "${fails}" ]; then
  echo
  echo "Tests failed: ${fails}"
  exit 1
else
  echo
  echo "Tests passed!"
  exit 0
fi