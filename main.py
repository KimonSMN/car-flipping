import requests
from bs4 import BeautifulSoup
import csv
import re

specific_model_total_price = 0
specific_model_count = 0
base_url = "https://www.car.gr/used-cars/"                  # Base Url of Car.gr 

make = "audi"
model = "a3"
year = "2011"

complete_url = f"{base_url}{make}/{model}/{year}.html?pg="
total_pages = 2                                            # Replace with actual number of pages

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
        milage_text = "Not Available"
        if len(milages) > 1:
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

with open("cars.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row

    # Prepare the deals CSV file
    with open("deals.csv", "w", newline='', encoding='utf-8') as deals_file:
        writer = csv.writer(deals_file)
        writer.writerow(header)  # Write the header to the deals file

        # Loop through each row in the original file
        for row in reader:
            if row:  # Check if row is not empty
                price = float(row[1].replace('€', '').replace('.', '').replace(',', '.'))  # Convert price to float
                # Check if the price is lower than the average and write to deals file
                if price < average_price:
                    writer.writerow(row)

# Print a message indicating the process is complete
print("Deals file created with cars priced below the average.")