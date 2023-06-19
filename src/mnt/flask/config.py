import os
from dotenv import load_dotenv, find_dotenv

class Config:

    load_dotenv(find_dotenv())
    # local computer dev
    #db_host = "localhost"
    #port = "32769"

    #docker dev
    db_host = "postgres"
    port = "5432"
    db_database = "airflow_db"
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_database}"
    SECRET_KEY = os.environ.get("SECRET_KEY")