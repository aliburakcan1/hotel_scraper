from entity_finder import EntityFinder
from hotel_scraper import HotelScraper
import pandas as pd
import time
import os
from html_parser import HTMLParser
import threading


ENTITY_DIR_PATH = "entities"
HTML_DIR_PATH = "html"

def save_html(html, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def find_entities(regions, stars):
    for region in regions:
        for star in stars:
            # Measure time
            start_time = time.time()
            name_entity = finder.get_entity_by_region_and_star(region, star)
            print(f"Time taken for finding entities: {time.time() - start_time}")
            print(f"Found {len(name_entity)} entities for {region} and {star} star hotels")
            df = pd.DataFrame(name_entity, columns=['name', 'entity'])
            df.to_csv(f'{ENTITY_DIR_PATH}/{region}_{star}.csv', index=False)

def scrape_hotels(entities, n_reviews):
    for entity in entities:
        html = scraper.scrape_with_reviews(entity, n_reviews)
        save_html(html, f"{HTML_DIR_PATH}/{entity}.html")

def read_and_scrape_hotels():
    for file in os.listdir(ENTITY_DIR_PATH):
        if file.endswith(".csv"):
            # Measure time
            start_time = time.time()
            entities = pd.read_csv(f"{ENTITY_DIR_PATH}/{file}")["entity"].tolist()
            scrape_hotels(entities, n_reviews = 10)
            print(f"Time taken for read and scrape hotels: {time.time() - start_time}")

#find_entities(regions, stars)
#read_and_scrape_hotels()

# Read all html files in html directory and parse them
def parse_html_files(method):
    ## Create output directory if it doesn't exist
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Measure time
    start_time = time.time()
    if method == "overview":
        GtHotelOverview, GtHotelTopThings, GtHotelSimilarHotels = parser.parse_overview()
        pd.DataFrame(GtHotelOverview).drop_duplicates().fillna("").to_csv("outputs/GtHotelOverview.csv", index=False)
        pd.DataFrame(GtHotelTopThings).drop_duplicates().fillna("").to_csv("outputs/GtHotelTopThings.csv", index=False)
        pd.DataFrame(GtHotelSimilarHotels).drop_duplicates().fillna("").to_csv("outputs/GtHotelSimilarHotels.csv", index=False)
    elif method == "reviews":
        GtHotelReviewSummary, GtHotelRatingsByTravelerType, GtHotelAspectTerms = parser.parse_review()
        pd.DataFrame(GtHotelReviewSummary).drop_duplicates().fillna("").to_csv("outputs/GtHotelReviewSummary.csv", index=False)
        pd.DataFrame(GtHotelRatingsByTravelerType).drop_duplicates().fillna("").to_csv("outputs/GtHotelRatingsByTravelerType.csv", index=False)
        pd.DataFrame(GtHotelAspectTerms).drop_duplicates().fillna("").to_csv("outputs/GtHotelAspectTerms.csv", index=False)
    elif method == "review_text":
        GtHotelReviews = parser.parse_review_text()
        pd.DataFrame(GtHotelReviews).drop_duplicates().fillna("").to_csv("outputs/GtHotelReviews.csv", index=False)
    elif method == "location":
        GtHotelLocationHighlights, GtHotelTransportation = parser.parse_location()
        pd.DataFrame(GtHotelLocationHighlights).drop_duplicates().fillna("").to_csv("outputs/GtHotelLocationHighlights.csv", index=False)
        pd.DataFrame(GtHotelTransportation).drop_duplicates().fillna("").to_csv("outputs/GtHotelTransportation.csv", index=False)
    elif method == "about":
        GtHotelFeaturesInfo, GtHotelFeatures = parser.parse_about()
        pd.DataFrame(GtHotelFeaturesInfo).drop_duplicates().fillna("").to_csv("outputs/GtHotelFeaturesInfo.csv", index=False)
        pd.DataFrame(GtHotelFeatures).drop_duplicates().fillna("").to_csv("outputs/GtHotelFeatures.csv", index=False)
        
    else:
        pass

    print(f"Time taken for parsing html files for {method}: {time.time() - start_time}")

def parallel_parse_html_files():
    threading.Thread(target=parser.parse_overview, args=[]).start()
    threading.Thread(target=parser.parse_review, args=[]).start()
    threading.Thread(target=parser.parse_review_text, args=[]).start()
    threading.Thread(target=parser.parse_location, args=[]).start()
    threading.Thread(target=parser.parse_about, args=[]).start()


#find_entities(regions, stars)
#read_and_scrape_hotels()
#parse_html_files("about")
if __name__ == '__main__':
    

    finder = EntityFinder()
    scraper = HotelScraper()
    parser = HTMLParser(HTML_DIR_PATH)

    #Create directories if they don't exist
    if not os.path.exists(ENTITY_DIR_PATH):
        os.makedirs(ENTITY_DIR_PATH)

    if not os.path.exists(HTML_DIR_PATH):
        os.makedirs(HTML_DIR_PATH)

    regions = ["barcelona"]
    stars = ["5"]

    #find_entities(regions, stars)
    #read_and_scrape_hotels()
    #parse_html_files("location")
    parallel_parse_html_files()
