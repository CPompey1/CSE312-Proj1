#!/bin/bash

for container in $(docker ps -q); do
  docker kill $container
done

echo "All docker containers killed"
