#!/bin/bash
docker push "$IMAGE_NAME:dev"
docker push "$IMAGE_NAME:$COMMIT"