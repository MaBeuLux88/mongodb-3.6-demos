#/usr/bin/env bash
docker exec -i mongo1 mongoimport --host replicaTest/mongo1:27017,mongo2:27017 --drop -d test -c arrayToObject < arrayToObject.json
docker exec -i mongo1 mongoimport --host replicaTest/mongo1:27017,mongo2:27017 --drop -d test -c objectToArray < objectToArray.json
