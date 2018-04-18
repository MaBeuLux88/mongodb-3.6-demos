#!/usr/bin/env bash

echo 'db.coll.aggregate(
    [
        {$group: {_id: null, min: {$min: "$a"}, max: {$max: "$a"}, tab: {$addToSet: "$a"}}},
        {
            $project: {
                _id: 0,
                min: 1,
                max: 1,
                missing: {$setDifference: [{$range: ["$min", "$max"]}, "$tab"]}
            }
        }
    ]
)
;' | docker exec -i mongo1 mongo --host replicaTest/mongo1:27017,mongo2:27017 --quiet | grep -v NETWORK 
