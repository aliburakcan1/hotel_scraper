
from lxml import html
import os
import time
import re

class HTMLParser():
    """Parses the html files and extracts the data"""

    def __init__(self, html_dir):
        self.html_dir = html_dir
        pass
    
    def parse_overview(self):
        """
        Parses the overview section of the html file
        Returns a dictionary with the following keys:
        entity, gt_name, star, city, province, district, address, phone, summary, score, price
        """
        html_dir = self.html_dir
        GtHotelOverview = {}
        GtHotelOverview["entity"] = []
        GtHotelOverview["gt_name"] = []
        GtHotelOverview["star"] = []
        GtHotelOverview["city"] = []
        GtHotelOverview["province"] = []
        GtHotelOverview["district"] = []
        GtHotelOverview["address"] = []
        GtHotelOverview["phone"] = []
        GtHotelOverview["summary"] = []
        GtHotelOverview["score"] = []
        GtHotelOverview["price"] = []

        GtHotelTopThings = {}
        GtHotelTopThings["entity"]  = []
        GtHotelTopThings["inference"] = []
        GtHotelTopThings["keywords"] = []
        GtHotelTopThings["related_review"] = []
        GtHotelTopThings["relation"] = []

        GtHotelSimilarHotels = {}
        GtHotelSimilarHotels["entity"]  = []
        GtHotelSimilarHotels["recommendation_entity"]  = []
        GtHotelSimilarHotels["recommendation_name"]  = []
        
        # Measure the time below loop
        time1 = time.time()
        for file in os.listdir(html_dir):
            if file.endswith(".html"):
                tree = html.parse(f"{html_dir}/{file}")
                entity = file.replace(".html", "")
                regions = [i.text for i in tree.xpath('//a[@class="CQYfx hAP9Pd" or @class="CQYfx hAP9Pd pxdxKe"]/span')]
                
                for sum_element in tree.xpath('//div[@class="iInyCf QqZUDd Zuc8V BLvVUb HoSN7e"]'):
                    name = sum_element.xpath('.//h1/text()')
                    star = sum_element.xpath('.//div[@class="fnmyY"]/span/text()')
                    address_phone = [i for i in sum_element.xpath('.//div[@class="K4nuhf"]/span/text()')]
                    summary = sum_element.xpath('.//div[@class="y3yqve QB2Jof"]/text()')
                    score = sum_element.xpath('.//div[@class="iDqPh BgYkof"]/text()')
                    price = sum_element.xpath('.//span[@class="qQOQpe prxS3d"]/text()')

                for top_element in tree.xpath('//div[@class="srD0rf eLNT1d"]'):
                    top_things = [[[j.text_content() for j in i.xpath('.//div[text()]')], [j.text_content() for j in i.xpath('.//span[text()]')]] for i in top_element.xpath('.//div[@class="PawDM"]')]

                similar_hotels = [[i.xpath('./@data-key'), i.xpath('.//div[@class="AdWm1c MFCiVb ogfYpf"]/text()')] for i in tree.xpath('//h2[contains(text(), "Similar to")]/../..//li')]

                GtHotelOverview["entity"].append(entity)
                GtHotelOverview["gt_name"].extend(name)
                GtHotelOverview["star"].append(star[0] if len(star) == 1 else "")
                GtHotelOverview["city"].append(regions[0] if len(regions) > 0 else "")
                GtHotelOverview["province"].append(regions[1] if len(regions) > 1 else "")
                GtHotelOverview["district"].append(regions[2] if len(regions) > 2 else "")
                GtHotelOverview["address"].append(address_phone[0] if len(address_phone) > 0 else "")
                GtHotelOverview["phone"].append(address_phone[-1] if len(address_phone) > 0 else "")
                GtHotelOverview["score"].append(score[0] if len(score) > 0 else "")
                GtHotelOverview["price"].append(price[0] if len(price) > 0 else "")
                GtHotelOverview["summary"].append(summary[0] if len(summary) > 0 else "")
                
                for i in range(len(top_things)):
                    GtHotelTopThings["entity"].append(entity)
                    GtHotelTopThings["inference"].append(top_things[i][0][0] if len(top_things[i][0])>0 else "")
                    GtHotelTopThings["keywords"].append(" || ".join(top_things[i][1]) if len(top_things[i][1])>0 else "")
                    GtHotelTopThings["related_review"].append(top_things[i][0][-2] if len(top_things[i][0])>2 else "")
                    GtHotelTopThings["relation"].append(top_things[i][0][-1] if len(top_things[i][0])>1 else "")
                    
                for i in range(len(similar_hotels)):
                    GtHotelSimilarHotels["entity"].append(entity)
                    GtHotelSimilarHotels["recommendation_entity"].append(similar_hotels[i][0][0])
                    GtHotelSimilarHotels["recommendation_name"].append(similar_hotels[i][1][0])

        time2 = time.time() - time1
        print(f"Time to parse overview: {time2}")
        return GtHotelOverview, GtHotelTopThings, GtHotelSimilarHotels

    def parse_review(self):
        """
        Parse the review page
        return: GtHotelReviewSummary, GtHotelRatingsByTravelerType, GtHotelReview
        """

        html_dir = self.html_dir

        GtHotelReviewSummary = {}
        GtHotelReviewSummary["entity"] = []
        GtHotelReviewSummary["rating_percentage_5"] = []
        GtHotelReviewSummary["rating_percentage_4"] = []
        GtHotelReviewSummary["rating_percentage_3"] = []
        GtHotelReviewSummary["rating_percentage_2"] = []
        GtHotelReviewSummary["rating_percentage_1"] = []
        GtHotelReviewSummary["review_count"] = []
        GtHotelReviewSummary["overall_rating"] = []
        GtHotelReviewSummary["room_rating"] = []
        GtHotelReviewSummary["location_rating"] = []
        GtHotelReviewSummary["service_rating"] = []

        GtHotelRatingsByTravelerType = {}
        GtHotelRatingsByTravelerType["entity"] = []
        GtHotelRatingsByTravelerType["traveler_type"] = []
        GtHotelRatingsByTravelerType["trip_type"] = []
        GtHotelRatingsByTravelerType["rating"] = []
        GtHotelRatingsByTravelerType["room_rating"] = []
        GtHotelRatingsByTravelerType["location_rating"] = []
        GtHotelRatingsByTravelerType["service_rating"] = []
        GtHotelRatingsByTravelerType["room_inference"] = []
        GtHotelRatingsByTravelerType["location_inference"] = []
        GtHotelRatingsByTravelerType["service_inference"] = []

        GtHotelAspectTerms = {}
        GtHotelAspectTerms["entity"] = []
        GtHotelAspectTerms["aspect_term"] = []
        GtHotelAspectTerms["aspect_review_count"] = []
        GtHotelAspectTerms["positive_review_count"] = []
        GtHotelAspectTerms["negative_review_count"] = []

        # Read html files from the folder then parse them
        for file in os.listdir(html_dir):
            if file.endswith(".html"):
                tree = html.parse(f"{html_dir}/{file}")
                entity = file.replace(".html", "")
                review_summary_xpath = '(//div[@class="pDLIp"])[1]'
                for element in tree.xpath(review_summary_xpath):
                    rating_percentages = [i.text_content() for i in element.xpath('.//span[@class="sSHqwe hSVOg"]')]
                    rating_percentages_5, rating_percentages_4, rating_percentages_3, rating_percentages_2, rating_percentages_1 = rating_percentages
                    review_count = element.xpath('.//div[@class="sSHqwe"]')[0].text_content()
                    overall_rating = element.xpath('.//div[@class="BARtsb"]')[0].text_content()
                    room_rating, location_rating, service_rating = None, None, None
                    for rls_div in tree.xpath('//div[@class="JErEuc"]//span[@class="UdVu2e pJYzRb"]'):
                        if rls_div.text_content() == "Rooms":
                            room_rating = rls_div.xpath('..//span[@class="w0q4db QB2Jof"]')[0].text_content()
                        elif rls_div.text_content() == "Location":
                            location_rating = rls_div.xpath('..//span[@class="w0q4db QB2Jof"]')[0].text_content()
                        elif rls_div.text_content() == "Service":
                            service_rating = rls_div.xpath('..//span[@class="w0q4db QB2Jof"]')[0].text_content()
                        else:
                            pass
                    GtHotelReviewSummary["entity"].append(entity)
                    GtHotelReviewSummary["rating_percentage_5"].append(rating_percentages_5)
                    GtHotelReviewSummary["rating_percentage_4"].append(rating_percentages_4)
                    GtHotelReviewSummary["rating_percentage_3"].append(rating_percentages_3)
                    GtHotelReviewSummary["rating_percentage_2"].append(rating_percentages_2)
                    GtHotelReviewSummary["rating_percentage_1"].append(rating_percentages_1)
                    GtHotelReviewSummary["review_count"].append(review_count)
                    GtHotelReviewSummary["overall_rating"].append(overall_rating)
                    GtHotelReviewSummary["room_rating"].append(room_rating)
                    GtHotelReviewSummary["location_rating"].append(location_rating)
                    GtHotelReviewSummary["service_rating"].append(service_rating)

                ratings_by_traveler_type_xpath = '//li[@class="Hj1rHb"]'
                for element in tree.xpath(ratings_by_traveler_type_xpath):
                    traveler_type = element.xpath('.//span[@class="fiHohf QB2Jof"]')[0].text_content()
                    trip_type = element.xpath('.//span[@class="fiHohf QB2Jof"]')[0].text_content()
                    rating = element.xpath('.//div[@class="fBDixb"]')[0].text_content()
                    room_rating, location_rating, service_rating = None, None, None
                    room_inference, location_inference, service_inference = None, None, None
                    for rls_div in element.xpath('.//section[@class="AAAwhe"]//span[@class="pjlrSd"]'):
                        if rls_div.text_content() == "Rooms":
                            room_rating = rls_div.xpath('..//span[@class="E6yyLe"]')[0].text_content()
                            room_inference = " || ".join([i.text_content() for i in rls_div.xpath('..//li[@class="xxF2uf"]')])
                        elif rls_div.text_content() == "Location":
                            location_rating = rls_div.xpath('..//span[@class="E6yyLe"]')[0].text_content()
                            location_inference = " || ".join([i.text_content() for i in rls_div.xpath('..//li[@class="xxF2uf"]')])
                        elif rls_div.text_content() == "Service":
                            service_rating = rls_div.xpath('..//span[@class="E6yyLe"]')[0].text_content()
                            service_inference = " || ".join([i.text_content() for i in rls_div.xpath('..//li[@class="xxF2uf"]')])
                        else:
                            pass
                    
                    GtHotelRatingsByTravelerType["entity"].append(entity)
                    GtHotelRatingsByTravelerType["traveler_type"].append(traveler_type)
                    GtHotelRatingsByTravelerType["trip_type"].append(trip_type)
                    GtHotelRatingsByTravelerType["rating"].append(rating)
                    GtHotelRatingsByTravelerType["room_rating"].append(room_rating)
                    GtHotelRatingsByTravelerType["location_rating"].append(location_rating)
                    GtHotelRatingsByTravelerType["service_rating"].append(service_rating)
                    GtHotelRatingsByTravelerType["room_inference"].append(room_inference)
                    GtHotelRatingsByTravelerType["location_inference"].append(location_inference)
                    GtHotelRatingsByTravelerType["service_inference"].append(service_inference)

                aspects_xpath = '//span[@class="Xm6fzc DjarMe"]'
                for element in tree.xpath(aspects_xpath):
                    aspect_term = element.xpath('.//div[@class="QB2Jof"]')[0].text_content()
                    aspect_review_count = element.xpath('.//div[@class="czYRub"]')[0].text_content()
                    aspect_percentage_count = element.xpath('.//div[@class="iAvhke"]/span')
                    negative_review_count, positive_review_count = aspect_percentage_count[0].text, aspect_percentage_count[1].text
                    GtHotelAspectTerms["entity"].append(entity)
                    GtHotelAspectTerms["aspect_term"].append(aspect_term)
                    GtHotelAspectTerms["aspect_review_count"].append(aspect_review_count)
                    GtHotelAspectTerms["positive_review_count"].append(positive_review_count)
                    GtHotelAspectTerms["negative_review_count"].append(negative_review_count)

        return GtHotelReviewSummary, GtHotelRatingsByTravelerType, GtHotelAspectTerms

    def parse_review_text(self):
        """
        Parse review text from the html files
        
        Returns:
            GtHotelReviews (dict): A dictionary of lists containing the parsed data
        """

        GtHotelReviews = {}
        GtHotelReviews["entity"] = []
        GtHotelReviews["review_text"] = []
        GtHotelReviews["owner_name"] = []
        GtHotelReviews["owner_link"] = []
        GtHotelReviews["rating"] = []
        GtHotelReviews["trip_type"] = []
        GtHotelReviews["review_date"] = []
        GtHotelReviews["room_score"] = []
        GtHotelReviews["location_score"] = []
        GtHotelReviews["service_score"] = []
        GtHotelReviews["response"] = []

        html_dir = self.html_dir

        # Read html files from the folder then parse them
        for file in os.listdir(html_dir):
            if file.endswith(".html"):
                review_tree = html.parse(f"{html_dir}/{file}").xpath('//div[@jsname="Pa5DKe"]')
                entity = file.replace(".html", "")
                for q, batch in enumerate(review_tree):
                    for w, review_div in enumerate(batch.xpath('.//div[@class="Svr5cf bKhjM"]')):
                        check = True
                        
                        for lower_link_div in review_div.xpath('.//div[@class="kVathc" or @class="kVathc eoY5cb"]'):
                            review_text = lower_link_div.xpath('.//div[@class="STQFb eoY5cb"]/div[@class="K7oBsc"]/div/span//text()')
                            if review_text:
                                review_text = " ".join(review_text)
                            else:
                                review_text = None
                            GtHotelReviews["review_text"].append(review_text)
                            

                            trip_type = lower_link_div.xpath('.//span[@class="VURE3b"]')
                            if trip_type:
                                trip_type = trip_type[0].text_content()
                            else:
                                trip_type = None
                            GtHotelReviews["trip_type"].append(trip_type)

                            review_aspects = [[i.xpath('.//span[1]')[0].text_content(), i.xpath('.//span[2]')[0].text_content()] for i in lower_link_div.xpath('.//div[@class="dA5Vzb"]')]
                            room_score = [j[1] for j in review_aspects if j[0] == "Rooms"]
                            location_score = [j[1] for j in review_aspects if j[0] == "Location"]
                            service_score = [j[1] for j in review_aspects if j[0] == "Service"]
                            GtHotelReviews["room_score"].append(room_score[0] if len(room_score)>0 else None)
                            GtHotelReviews["location_score"].append(location_score[0] if len(location_score)>0 else None)
                            GtHotelReviews["service_score"].append(service_score[0] if len(service_score)>0 else None)
                            response_text = " ".join(lower_link_div.xpath('..//div[@class="n7uVJf"]/*[text()]/text()'))
                            GtHotelReviews["response"].append(response_text if response_text != "" else None)
                            check = False

                        if check:
                            continue
                        GtHotelReviews["entity"].append(entity)
                        
                        for upper_review_div in review_div.xpath('.//div[@class="aAs4ib"]'):
                            name_link_div = upper_review_div.xpath('.//a[@class="DHIhE QB2Jof"]')

                            if len(name_link_div) < 1:
                                owner_link = upper_review_div.xpath('.//span[@class="iUtr1 CQYfx"]/a')[0].get('href') if len(upper_review_div.xpath('.//span[@class="iUtr1 CQYfx"]/a'))>0 else None
                                owner_name = upper_review_div.xpath('.//span[@class="faBUBf QB2Jof"]')[0].text if len(upper_review_div.xpath('.//span[@class="faBUBf QB2Jof"]'))>0 else None
                            else:
                                owner_link = name_link_div[0].get('href')
                                owner_name = name_link_div[0].text
                            rating = upper_review_div.xpath('.//div[@class=" GDWaad"]')[0].text
                            review_date = upper_review_div.xpath('.//span[@class="iUtr1 CQYfx"]')[0].text_content()
                            
                            GtHotelReviews["owner_name"].append(owner_name)
                            GtHotelReviews["owner_link"].append(owner_link)
                            GtHotelReviews["rating"].append(rating)
                            GtHotelReviews["review_date"].append(review_date)
        return GtHotelReviews

    def parse_location(self):
        """
        Parse location information from the html files
        
        Returns:
            GtHotelLocationHighlights (dict): A dictionary of location highlights
            GtHotelTransportation (dict): A dictionary of transportation information
        """
        html_dir = self.html_dir
        GtHotelLocationHighlights = {}
        GtHotelLocationHighlights["entity"] = []
        GtHotelLocationHighlights["location_title"] = []
        GtHotelLocationHighlights["location_overview"] = []
        GtHotelLocationHighlights["score"] = []
        GtHotelLocationHighlights["things_to_do_score"] = []
        GtHotelLocationHighlights["restaurants_score"] = []
        GtHotelLocationHighlights["transportation_score"] = []
        GtHotelLocationHighlights["airport_score"] = []

        GtHotelTransportation = {}
        GtHotelTransportation["entity"] = []
        GtHotelTransportation["place_type_of_arrival"] = []
        GtHotelTransportation["place_of_arrival"] = []
        GtHotelTransportation["transportation_type"] = []
        GtHotelTransportation["eta"] = []


        for file in os.listdir(html_dir):
            if file.endswith(".html"):
                entity = file.replace(".html", "")
                tree = html.parse(f"{html_dir}/{file}")
                location_tree_xpath = '//div[@class="fe4pJf fjPU1d daXQs"]'
                for element in tree.xpath(location_tree_xpath):
                    location_title = element.xpath('.//span[@class="tdXnEc"]')[0].text_content() if len(element.xpath('.//span[@class="tdXnEc"]'))>0 else None
                    location_overview = element.xpath('./span[1]/div[1]/div/span')[0].text_content() if len(element.xpath('./span[1]/div[1]/div'))>0 else None
                    score = element.xpath('.//div[@class="mZf8qb"]/*/*[1]')[0].text_content()
                    things_to_do_score = element.xpath('.//div[@class="mZf8qb"]/*/*[2]')[0].text_content()
                    score_list = [i.text for i in element.xpath('.//div[@class="Kf0JYe Sdjmkb wdLSAe"]//span[2]')]
                    things_to_do_score, restaurants_score, transportation_score, airport_score = score_list
                
                    GtHotelLocationHighlights["entity"].append(entity)
                    GtHotelLocationHighlights["location_title"].append(location_title)
                    GtHotelLocationHighlights["location_overview"].append(location_overview)
                    GtHotelLocationHighlights["score"].append(score)
                    GtHotelLocationHighlights["things_to_do_score"].append(things_to_do_score)
                    GtHotelLocationHighlights["restaurants_score"].append(restaurants_score)
                    GtHotelLocationHighlights["transportation_score"].append(transportation_score)
                    GtHotelLocationHighlights["airport_score"].append(airport_score)
                
                airport_tree_xpath = './/div[@jscontroller="AYHkGd"]/div[@class="QI4ND"]'
                for element in tree.xpath(airport_tree_xpath):
                    place_type_of_arrival = "airport"
                    place_of_arrival = element.xpath('.//span[@class="QB2Jof cemq3"]')[0].text
                    for subelement in element.xpath('.//div[@class="xje3dc"]'):
                        transportation_type = subelement.xpath('.//span[@class="rlyene"]')[0].text_content()
                        eta = subelement.xpath('.//span[@class="sWrG2e"]')[0].text_content()
                        GtHotelTransportation["entity"].append(entity)
                        GtHotelTransportation["place_type_of_arrival"].append(place_type_of_arrival)
                        GtHotelTransportation["place_of_arrival"].append(place_of_arrival)
                        GtHotelTransportation["transportation_type"].append(transportation_type)
                        GtHotelTransportation["eta"].append(eta)
                
                transit_tree_xpath = './/span[@jsname="PAiuue"]/div[@class="QI4ND"]/div[@class="kgXiLe"]'
                for element in tree.xpath(transit_tree_xpath):
                    place_type_of_arrival = "transit"
                    for subelement in element.xpath('.//div[@class="xje3dc"]'):
                        place_of_arrival = subelement.xpath('.//span[@class="rlyene"]')[0].text_content()
                        
                        label = subelement.xpath('.//span[@class="kJW6fe"]/@aria-label')[0]
                        eta = " ".join(label.split(" ")[:-1])
                        transportation_type = " ".join(label.split(" ")[-1:])
                        GtHotelTransportation["entity"].append(entity)
                        GtHotelTransportation["place_type_of_arrival"].append(place_type_of_arrival)
                        GtHotelTransportation["place_of_arrival"].append(place_of_arrival)
                        GtHotelTransportation["transportation_type"].append(transportation_type)
                        GtHotelTransportation["eta"].append(eta)


        return GtHotelLocationHighlights, GtHotelTransportation
