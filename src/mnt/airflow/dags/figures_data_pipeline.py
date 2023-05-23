from airflow import DAG
from datetime import datetime, timedelta
import requests, bs4, json
from collections import namedtuple
import random
import time

from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

Product = namedtuple("Product", "Title Price Status Source Download")
download_date = datetime.today().strftime('%Y-%m-%d')

def get_figures_prices_mtg():

    res = requests.get('https://strefamtg.pl/2027-space-marines')
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')

    pages = noStarchSoup.find("ul", {"class": "pagination__list"}).find_all("a", {"class": "js-search-link"})
    pages_numbers = [int(page.text.strip()) for page in pages if page.text.strip().isnumeric()]
    products = []
    for page in pages_numbers:
        url = f'https://strefamtg.pl/2027-space-marines?page={page}'
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        items = soup.find(id="js-product-list").find_all("div", {"class": "product-miniature__inner"})

        for item in items:

            fields = [field for field in item.contents if field != '\n']
            title = [field for field in fields if "product-miniature__title" in field['class']][0].text.strip()
            prices_all = [field for field in fields if "product-miniature__prices" in field['class']][0].children
            price_str = [field for field in prices_all if field != '\n' and "price" in field['class']][0].text.strip()
            status_str = [field for field in fields if "product-quantities" in field['class']][0].text.strip()

            price = float(price_str.replace("\xa0zł", "").replace(",", "."))
            status = "Produkt niedostępny" if status_str.strip() == "Produkt niedostępny" else status_str.split(":")[1].strip()

            product = Product(title, price, status, "MTG", download_date)
            products.append(product._asdict())

    with open(r'/opt/airflow/dags/files/mtg_figures_prices.json', 'w', encoding='utf8') as outfile:
        json.dump(products, outfile, indent=4, ensure_ascii=False)


def get_figures_prices_fgb():
    res = requests.get('https://fgb.club/warhammer-40000-sklep-fgb-warszawa/Warhammer-40000-Space-Marines-sklep-warszawa-fgb?limit=200')
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    items = noStarchSoup.find("div", {"class": "main-products"}).find_all("div", {"class": "product-details"})
    items_details = [item.find("div", {"class": "caption"}) for item in items]
    products = []
    for i_details in items_details:
        title = i_details.find("h4", {"class": "name"}).text.strip()
        prices = i_details.find("div", {"class": "price"}).children
        price = min([float(p.text.replace("zł","").strip()) for p in prices if p.text.strip() != ''])
        status = i_details.find("div", {"class": "availability"}).text.strip()
        product = Product(title, price, status, "FGB", download_date)
        products.append(product._asdict())
    
    with open(r'/opt/airflow/dags/files/fgb_figures_prices.json', 'w', encoding='utf8') as outfile:
        json.dump(products, outfile, indent=4, ensure_ascii=False)

with DAG("figures_data_pipeline", start_date=datetime(2023, 1, 1),
         schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    
    is_mtg_website_available =  HttpSensor(
        task_id="is_mtg_website_available",
        http_conn_id="mtg_website",
        endpoint="",
        response_check=lambda response: True if 200 == response.status_code else False,
        poke_interval=5,
        timeout=30
    )


    is_fgb_website_available =  HttpSensor(
        task_id="is_fgb_website_available",
        http_conn_id="fgb_website",
        endpoint="",
        response_check=lambda response: True if 200 == response.status_code else False,
        poke_interval=5,
        timeout=30
    )

    creating_figures_details_table = PostgresOperator(
        task_id="creating_figures_details_table",
        postgres_conn_id="postgres_db",
        sql="""
            CREATE TABLE IF NOT EXISTS figures_details (
            id SERIAL PRIMARY KEY,
            title VARCHAR,
            Price DECIMAL,
            Availability INT,
            Source VARCHAR,
            Download DATE,
            Comments VARCHAR );
          """
    )

    saving_mtg_figures_prices = PythonOperator(
        task_id="saving_mtg_figures_prices",
        python_callable=get_figures_prices_mtg
    )
    saving_fgb_figures_prices = PythonOperator(
        task_id="saving_fgb_figures_prices",
        python_callable=get_figures_prices_fgb
    )


    figures_processing = SparkSubmitOperator(
        task_id="figures_processing",
        application="/opt/airflow/dags/scripts/process_figures_data.py",
        conn_id="spark_conn",
        jars="/opt/spark/jars/postgresql-42.2.5.jar"
    )

    is_mtg_website_available >> saving_mtg_figures_prices >> creating_figures_details_table >> figures_processing
    is_fgb_website_available >> saving_fgb_figures_prices >> creating_figures_details_table >> figures_processing