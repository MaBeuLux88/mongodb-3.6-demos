#!/usr/bin/env bash
docker exec -it mongo1 mongo --host replicaTest/mongo1:27017,mongo2:27017
