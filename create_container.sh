#!/bin/sh

container=fireflyiii-spectre

docker create --env-file env_file -p 8082:8080 -v $(pwd)/configs:/configs --name $container fireflyiii/spectre-importer:latest
