#!/usr/bin/env bash

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get -y install docker-ce
echo '{ "features": { "buildkit": true }, "experimental": true }' | sudo tee /etc/docker/daemon.json
sudo service docker restart

if [[ "$TRAVIS_PULL_REQUEST" == "false" ]]; then
    echo $DOCKER_PASSWORD | docker login --username="$DOCKER_LOGIN" --password-stdin
fi