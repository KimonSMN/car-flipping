import requests
from bs4 import BeautifulSoup
import csv

total_price = 0
num_prices = 0
base_url = "https://www.car.gr/used-cars/audi.html?activeq=audi&category=15001&from_suggester=1&make=14093&pg="
total_pages = 1 # Replace with actual number of pages or a method to find it

file = open("audi_cars.csv", "w", newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(["TITLE", "PRICE", "CAR ID"])  # Combine headers into one row

for page_num in range(1, total_pages + 1):
    page_url = base_url + str(page_num)
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")

    titles = soup.findAll("h2", attrs={"class": "title"})
    prices = soup.findAll("div", attrs={"class": "price-tag current-price"})
    car_ids = soup.findAll("a", attrs={"class": "row-anchor"})
    milages = soup.findAll("span", attrs={"title": "Milage"})
    
    for price_tag in prices:
        # Extract and clean the price
        price_text = price_tag.get_text(strip=True).replace('€', '').replace('.', '').replace(',', '.')
        price = float(price_text)
        total_price += price
        num_prices += 1

    for title, price, car_id_tag in zip(titles, prices, car_ids):
        if "Audi" in title.text:
            car_id = car_id_tag['href'].split('/')[-1] if car_id_tag else 'N/A'
            writer.writerow([title.text.strip(), price.text.strip(), car_id])

if num_prices > 0:
    average_price = total_price / num_prices
    print("Average Price:", average_price)
else:
    print("No prices found to calculate the average.")

file.close()