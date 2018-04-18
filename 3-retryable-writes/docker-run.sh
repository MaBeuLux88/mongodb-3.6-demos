#!/usr/bin/env bash
docker run -h mongodb-python --rm --name mongodb-python --network mongonet --network-alias mongodb-python mabeulux88/mongodb-python:1.0
