#!/bin/bash
# Author : Maxime BEUGNET <maxime.beugnet@gmail.com>
mongoimport --quiet -d test -c persons persons.1000.json
