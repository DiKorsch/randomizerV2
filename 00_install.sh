#!/usr/bin/env bash

docker build -f Dockerfile --tag dikorsch/randomizer .

docker-compose build $@ && docker-compose config
