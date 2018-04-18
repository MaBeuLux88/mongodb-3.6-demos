#!/usr/bin/env bash
docker stop mongo1 mongo2 mongo3
docker rm -v mongo1 mongo2 mongo3
rm -rf data 
