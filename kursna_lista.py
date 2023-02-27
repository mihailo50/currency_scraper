import requests, datetime, os
from bs4 import BeautifulSoup

# get site
url = "https://www.kursna-lista.com/kursna-lista-nbs"
response = requests.get(url)

# scrape
soup = BeautifulSoup(response.content, "html.parser")
elements = soup.find_all()
table = soup.table
rows = table.find_all("tr")

# create list for data
kursna_lista = []

# create time format
today = datetime.date.today()
date_format = today.strftime("%Y/%m/%d")
if today.month >= 9:
    fiscal_year = today.year + 1
else:
    fiscal_year = today.year
year_folder = f"FY {fiscal_year % 100:02d}"
month_folder = today.strftime("%B %Y").upper()
# fiscal condition


for row in rows:
    cells = row.find_all("td")
    if len(cells) == 0:
        continue
    kurs = f'"{cells[1].text}",'
    kurs += f'"RSD",'
    kurs += f'"{cells[4].text}",'
    kurs += f'"{date_format}"'
    kursna_lista.append(kurs)

date_format = today.strftime("%Y%m%d")
file_name = "RSD currency rates "+date_format+".txt"

if not os.path.exists(year_folder):
    os.mkdir(year_folder)

if not os.path.exists(os.path.join(year_folder, month_folder)):
    os.mkdir(os.path.join(year_folder, month_folder))

with open(os.path.join(year_folder, month_folder, file_name), "w") as f:
    for item in kursna_lista:
        # item = item.strip('"')
        f.write(f"{item}\n")
        