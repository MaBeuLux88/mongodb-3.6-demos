#!/usr/bin/env bash

# Here we start our main MongoDB instances in v3.6
docker run -d -p 27017:27017 -h mongo1 --network mongonet --network-alias mongo1 --name mongo1 \
	mongo:3.6.3 --replSet replicaTest --bind_ip_all

docker run -d -p 27018:27017 -h mongo2 --network mongonet --network-alias mongo2 --name mongo2 \
	mongo:3.6.3 --replSet replicaTest --bind_ip_all

docker run -d -p 27019:27017 -h mongo3 --network mongonet --network-alias mongo3 --name mongo3 \
	mongo:3.6.3 --replSet replicaTest --bind_ip_all

sleep 1

# Here we initialize the replica
echo 'rs.initiate({
      _id: "replicaTest",
      members: [
         { _id: 0, host: "mongo1:27017" },
         { _id: 1, host: "mongo2:27017" },
         { _id: 2, host: "mongo3:27017", arbiterOnly:true }]});' | mongo

