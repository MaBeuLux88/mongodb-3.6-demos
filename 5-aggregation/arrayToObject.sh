#!/usr/bin/env bash
docker exec -i mongo1 mongo --host replicaTest/mongo1:27017,mongo2:27017 --quiet < arrayToObject.js
