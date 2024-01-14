import requests
from bs4 import BeautifulSoup
import csv
import re

specific_model_total_price = 0
specific_model_count = 0
base_url = "https://www.car.gr/used-cars/"                  # Base Url of Car.gr 
make_url = "toyota" #input("Enter Car Make you want to search for: ") # Car Make Url
rest_of_url = ".html?pg="                                   # Rest of Url needed for complete form of Url
complete_url = base_url + make_url + rest_of_url            # The complete url
total_pages = 4                                             # Replace with actual number of pages

car_model = "Yaris " #input("Enter Car Model you want to search for: ")
car_year = "'12" #input("Enter Car Model's Year you want to search for: ")

file = open("cars.csv", "w", newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(["TITLE", "PRICE", "CAR ID"])  #Write header

for page_num in range(1, total_pages + 1): 
    page_url = complete_url + str(page_num)
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Scrape information out of the site
    titles = soup.findAll("h2", attrs={"class": "title"}) # Title of the car
    prices = soup.findAll("div", attrs={"class": "price-tag current-price"})
    car_ids = soup.findAll("a", attrs={"class": "row-anchor"})
    
    # Write car information to the csv file
    for title, price_tag, car_id_tag in zip(titles, prices, car_ids):
        if car_model in title.text and car_year in title.text:
            price_text = price_tag.get_text(strip=True)
            price_value = price_text.replace('€', '').replace('.', '').replace(',', '.')
            price = float(price_value)
            href = car_id_tag['href']
            match = re.search(r'(\d+)-', href)
            car_id = match.group(1)
            
            # open car url
            new_page_url = "https://www.car.gr/classifieds/cars/view/" + car_id
            page = requests.get(new_page_url)
            soup = BeautifulSoup(page.content, "html.parser")
            
            # search for milage
            milages = soup.find_all("div", attrs={"class": "tw-text-black kicon-value tw-line-clamp-2 [word-break:break-word]"})
            selected_milage = milages[1]
            milage_text = selected_milage.get_text(strip=True)
            
            # write info to file
            writer.writerow([title.text.strip(), price_text, car_id, milage_text])
            specific_model_total_price += price
            specific_model_count += 1 

# Find Average Price of the Cars
if specific_model_count > 0:
    average_price = specific_model_total_price / specific_model_count
    print("Average Price of specific models:", average_price)
else:
    print("No specific models found to calculate the average.")

file.close()

