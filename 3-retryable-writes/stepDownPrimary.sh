#!/usr/bin/env bash
echo 'rs.stepDown(3,2)' | docker exec -i mongo1 mongo --host replicaTest/mongo1:27017,mongo2:27017 --quiet
