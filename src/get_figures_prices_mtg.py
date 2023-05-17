import bs4, requests
from collections import namedtuple
import json

Product = namedtuple("Product", "Title Price Status")

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

        product = Product(title, price, status)
        products.append(product)

with open(r'src/mnt/airflow/dags/files/mtg_figures_prices.json', 'w', encoding='utf8') as outfile:
    json.dump(products, outfile, indent=4, ensure_ascii=False)



