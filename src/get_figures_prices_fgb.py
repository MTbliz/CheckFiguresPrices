import bs4, requests
from collections import namedtuple
import json

Product = namedtuple("Product", "Title Price Status")

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
    product = Product(title, price, status)
    products.append(product)

with open(r'src/mnt/airflow/dags/files/fgb_figures_prices.json', 'w', encoding='utf8') as outfile:
    json.dump(products, outfile, indent=4, ensure_ascii=False)
