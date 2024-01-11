import requests
import json
from bs4 import BeautifulSoup


# Function to scrape the definitions for a given word URL
def scrape_definitions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    definition_divs = soup.find_all("div", class_="break-words meaning mb-4")
    definitions = [div.text.strip() for div in definition_divs]
    return definitions


# Main scraping function
def scrape_website():
    base_url = "https://www.urbandictionary.com"
    characters = [chr(i) for i in range(ord("A"), ord("Z") + 1)] + ["#"]

    definitions_dict = {}

    for character in characters:
        print(f"{character} is initialized")
        page_number = 1

        while True:
            url = f"{base_url}/browse.php?character={character}&page={page_number}"
            response = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
                },
            )
            soup = BeautifulSoup(response.content, "html.parser")
            word_links = soup.find_all(
                "a",
                class_="py-1 block text-denim dark:text-white break-all hover:text-limon-lime hover:underline",
            )

            if not word_links:
                break

            for link in word_links:
                word_url = base_url + link["href"]
                definitions = scrape_definitions(word_url)
                if link.text not in definitions_dict:
                    definitions_dict[link.text] = []
                definitions_dict[link.text].extend(definitions)

                # Save the definitions as JSON
        with open("definitions_new_d.json", "w") as json_file:
            json.dump(definitions_dict, json_file)

            page_number += 1

    print("Definitions saved as definitions.json")


# Run the scraping function
scrape_website()
