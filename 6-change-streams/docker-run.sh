#!/usr/bin/env bash
docker run --rm --network mongonet mabeulux88/mongodb-change-streams:1.0 mongodb://mongo1,mongo2 $1

