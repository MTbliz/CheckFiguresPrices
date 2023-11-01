#!/usr/bin/env bash

#check if linux or windows format
# Initiliase the metastore
airflow db init

# Run the scheduler in background
airflow scheduler &> /dev/null &

# Create user
airflow users create -u admin -p admin -r Admin -e admin@admin.com -f admin -l admin

# Add airflow connections
airflow connections add 'fgb_website' \
    --conn-json '{
        "conn_type": "HTTP",
        "host": "https://fgb.club/"
    }'

airflow connections add 'mtg_website' \
    --conn-json '{
        "conn_type": "HTTP",
        "host": "https://strefamtg.pl/"
    }'

airflow connections add 'postgres_db' \
    --conn-json '{
        "conn_type": "postgres",
        "login": "airflow",
        "password": "airflow",
        "host": "postgres",
        "schema": "airflow_db"
    }'

airflow connections add 'spark_conn' \
    --conn-json '{
        "conn_type": "spark",
        "host": "spark://spark-master",
        "port": "7077"
    }'

# Run the web server in foreground (for docker logs)
exec airflow webserver