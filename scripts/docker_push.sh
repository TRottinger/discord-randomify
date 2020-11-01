#!/bin/bash
echo $DOCKER_PASSWORD | docker login --username="$DOCKER_LOGIN" --password-stdin
docker push "$IMAGE_NAME:$TRAVIS_COMMIT"