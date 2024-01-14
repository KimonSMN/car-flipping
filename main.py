import requests
from bs4 import BeautifulSoup
import csv

specific_model_total_price = 0
specific_model_count = 0
base_url = "https://www.car.gr/used-cars/audi.html?activeq=audi&category=15001&from_suggester=1&make=14093&pg="
total_pages = 1  # Replace with actual number of pages or a method to find it

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

    for title, price_tag, car_id_tag in zip(titles, prices, car_ids):
        if "Audi" in title.text:
            price_text = price_tag.get_text(strip=True)
            price_value = price_text.replace('€', '').replace('.', '').replace(',', '.')
            try:
                price = float(price_value)
                car_id = car_id_tag['href'].split('/')[-1] if car_id_tag else 'N/A'
                writer.writerow([title.text.strip(), price_text, car_id])  # Use price_text here

                if "16" in title.text:
                    specific_model_total_price += price
                    specific_model_count += 1
            except ValueError:
                # Handle the case where the conversion fails
                print(f"Could not convert price '{price_text}' to a number.")

if specific_model_count > 0:
    average_price = specific_model_total_price / specific_model_count
    print("Average Price of specific models:", average_price)
else:
    print("No specific models found to calculate the average.")

file.close()
