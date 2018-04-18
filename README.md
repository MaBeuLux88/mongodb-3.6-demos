# Demos MongoDB 3.6 new features

This repository consists in a bunch of scripts to execute to test new MongoDB 3.6 features.

# Prerequisites

 * Linux
 * Docker
 * Aaaaaand, that's all folks

# Knowledge necessary

 * Basic MongoDB
 * Basic Python

# How to Use

## Creating the network

 * Go to 1-network and execute `create.sh`
 * If need be, you can remove the network by using `clean.sh`

## Creating the MongoDB Database

 * Go to 2-start-mongo and execute `docker-run.sh`.
 * If need be, you can use `docker-clean.sh` to totally erase the MongoDB instances (the data will be lost).

## Testing retryable write

 * Go to 3-retryable-writes 
 * Run `./docker-build.sh` once to create the docker image.
 * This image runs the `retryableWrites.py` python script that writes into MongoDB.
 * Run this container with `./docker-run.sh [true|false]` and choose the boolean to activate or not the retryable writes.
 * This script writes a suite of very simple documents `{a: X}` where X increases from 0 to 10000.
 * Run the `./stepDownPrimary.sh` a few times to switch the primary server with the secondary.
 * If you have activated the retryable writes, then the `./findMissing.sh` will return an empty list.
 * If you did not activate the retryable writes, then the `./findMissing.sh` will return the list of missing numbers. 

## [WIP] Testing causal consistency

 * Go to 4-causal-consistency and look at the script `hereWeCode.py`, it reads from MongoDB, without option, to get the actual state of data
 * It then opens a session, updates the document that we just read (or inserts if the document didn't exist)
 * It then reads the document we just upserted (with readPreference to 'secondary').
 * Put causalConsistency to False to test things out.
 * Build the image with `docker-build.sh`
 * Run the script with `docker-run.sh` (Don't hesitate to run it multiple times). You'll see that there's no difference between the first and the second print, despite the update
 * Put causalConsistency to True.
 * Build the image with `docker-build.sh`
 * Run the script with `docker-run.sh` (Don't hesitate to run it multiple times). Now the two prints will be different, as the session is waiting for replication. 
 * NOTE : In this case, putting the write concern to 2 would have also worked.

## Trying aggregation stages

### Array to Object
 * Use the `docker-run.sh` to load some data in MongoDB
 * Use `connect_to_mongodb.sh` to launch the shell
 * Launch this command to test `$arrayToObject`:
```javascript
db.arrayToObject.aggregate(
   [
      {
         $project: {
            item: 1,
            dimensions: { $arrayToObject: "$dimensions" }
         }
      }
   ]
)
```
 * Launch this command to test `$objectToArray`:
```javascript
db.objectToArray.aggregate(
   [
      {
         $project: {
            item: 1,
            dimensions: { $objectToArray: "$dimensions" }
         }
      }
   ]
)
```

