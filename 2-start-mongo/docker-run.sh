#!/usr/bin/env bash

mkdir -p data/{db1,db2,db3}

# Here we start our main MongoDB instance, in >3.6
docker run -d -p 27017:27017 -v $(pwd)/data/db1:/data/db1 \
	-u 1000:1000 -h mongo1 --network mongonet \
	--network-alias mongo1 --name mongo1 \
	mongo:3.6.3 --dbpath /data/db1 --replSet replicaTest --bind_ip_all --logpath /data/db1/mongod.log

docker run -d -p 27018:27017 -v $(pwd)/data/db2:/data/db2 \
	-u 1000:1000 -h mongo2 --network mongonet \
	--network-alias mongo2 --name mongo2 \
	mongo:3.6.3 --dbpath /data/db2 --replSet replicaTest --bind_ip_all --logpath /data/db2/mongod.log

docker run -d -p 27019:27017 -v $(pwd)/data/db3:/data/db3 \
	-u 1000:1000 -h mongo3 --network mongonet \
	--network-alias mongo3 --name mongo3 \
	mongo:3.6.3 --dbpath /data/db3 --replSet replicaTest --bind_ip_all --logpath /data/db3/mongod.log

sleep 1

# Here we initialize the replica
echo 'rs.initiate({
      _id: "replicaTest",
      members: [
         { _id: 0, host: "mongo1:27017" },
         { _id: 1, host: "mongo2:27017" },
         { _id: 2, host: "mongo3:27017", arbiterOnly:true }]});' | mongo

