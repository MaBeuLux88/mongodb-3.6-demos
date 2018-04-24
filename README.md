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

## Testing causal consistency

 * Go to 4-causal-consistency
 * Run `./docker-build.sh` once to create the docker image.
 * This image runs the `causalConsistency.py` python script.
 * Run this container with `./docker-run.sh [true|false]` and choose the boolean to activate or not the causal consistency.
 * This script does the following actions:
   * Open a session,
   * Read the current document on the primary (=real value stored),
   * Increment x by 10 on primary node (of course)
   * Read the current document on the secondary (=eventually consistent value - depends if the replication is done already or not),
   * Close session.
 * If the causal consistency is not activated, the read on the secondary returns the old value of X. The do NOT read our own write.
 * If the causal consistency is activated, the read on the secondary returns the new value of X. We are reading our own write.

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

