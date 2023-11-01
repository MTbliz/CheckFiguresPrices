#!/usr/bin/env bash

sleep 10
# Check if the database exists
if influx -execute 'SHOW DATABASES' | grep -q 'telegraf'; then
  echo "Database exists"
else
  influx -execute 'create database telegraf'
fi