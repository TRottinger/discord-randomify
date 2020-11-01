#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_LOGIN" --password-stdin
docker push $DOCKER_REPO/discord-randomizer