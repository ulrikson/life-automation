# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import time
import csv
import re


def collect_user_inputs():
    """Collects inputs from the user regarding the URL and number of pages to scrape"""
    city_url = input("What is the url to the city on hemnet? ")
    pages = int(input("How many pages do you want to scrape? "))
    return city_url, pages


def scrape_page(url, headers):
    """Makes a request to the specified URL with the provided headers and returns parsed HTML content"""
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, "html.parser")


def extract_prices_from_results(results):
    """Extracts prices from the results of the scraped page"""
    data = []
    for result in results:
        price = result.find("div", class_="listing-card__attribute listing-card__attribute--primary").text
        # Remove all non-numeric characters
        price = re.sub("[^0-9]", "", price)
        data.append(price)
    return data


def save_data_to_csv(data, filename):
    """Saves the data into a CSV file with the provided filename"""
    with open(filename + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["price"])
        for price in data:
            writer.writerow([price])
    print("Done")


def main():
    # Collect user inputs
    city_url, pages = collect_user_inputs()

    # Prepare the headers for the request
    headers = {"User-Agent": "Mozilla/5.0"}

    # Prepare a list to store the data
    data = []

    for x in range(1, pages + 1):
        # Generate the URL for the current page
        url = city_url + "&page=" + str(x)

        # Scrape the current page
        soup = scrape_page(url, headers)

        # Check if there are no more pages
        if soup.find("h2", string="Inga träffar på din sökning"):
            print("No more pages")
            break

        # Find all relevant divs on the page
        results = soup.find_all("div", class_="listing-card__information-content")

        # Extract prices from the results and add them to our data
        data.extend(extract_prices_from_results(results))

        # Pause for 5 seconds to avoid raising suspicion
        time.sleep(5)

        # Indicate that the current page has been processed
        print(f"Page {x} done")

    # Ask the user what the file should be called
    filename = input("What should the file be called? (without .csv) ")

    # Save the data to a CSV file
    save_data_to_csv(data, filename)


if __name__ == "__main__":
    main()
