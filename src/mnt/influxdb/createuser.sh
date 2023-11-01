#!/bin/bash

# Check if the database exists
if influx -execute 'SHOW USERS' | grep -q 'telegraf'; then
  echo "USER exists"
else
  influx -execute 'create user telegraf with password telegrafpass'
fi