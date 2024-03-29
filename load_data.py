# # use the full column search technique from books review website, using like key word
# # design the page to display search results
# # if there is no result and the data matches an address format, use nhs online local help to search and store in database, and display results
#
# # design the page to add new place
# # create wtf form for user to add a review to an existing form
# # design the page to write a review
# #
#
import requests
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from app import app
from app import db
from app import Resources, Reviews

with app.app_context():
    db.create_all()

# scraping google map
google_map_api_key = API_KEY
location = '51.5072%2C0.1276'  # London's lag and log
base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
next_page_base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'


def load_google_map_data(url):
    time.sleep(5)
    response = requests.get(url)
    data = response.json()

    with app.app_context():
        for place in data['results']:
            existing_resource = Resources.query.filter_by(name=place['name']).first()
            if existing_resource is None:
                resource = Resources(name=place['name'], description=place.get('formatted_address'))
                db.session.add(resource)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Error adding resource: {e}')
    return data.get('next_page_token')


first_url = f'{base_url}location={location}&query=mental%20health&radius=10000&key={google_map_api_key}'
next_page_token = load_google_map_data(first_url)

while next_page_token:
    next_page_url = f'{next_page_base_url}pagetoken={next_page_token}&key={google_map_api_key}'
    print(next_page_url)
    next_page_token = load_google_map_data(next_page_url)


# scrape hub of hope
hub_url = 'https://hubofhope.co.uk/services?concerns=9%2C37%2C5&latitude=51.5072178&longitude=-0.1275862&page=1'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(hub_url)
time.sleep(5)
cookie_button = driver.find_element(By.CSS_SELECTOR, value='.cc-btn.cc-ALLOW')
cookie_button.click()
time.sleep(2)
link_elements = driver.find_elements(By.CSS_SELECTOR, value="a.service-card__link")
links = [link_element.get_attribute('href') for link_element in link_elements]
name_elements = driver.find_elements(By.CLASS_NAME, value="service-card__title")
names = [name_element.text for name_element in name_elements]

for name, link in zip(names, links):
    try:
        driver.get(link)
        time.sleep(5)
        website_element = driver.find_element(By.CSS_SELECTOR, value="a.service__information-content")
        website = website_element.get_attribute('href')
    except NoSuchElementException:
        website = ""
    with app.app_context():
        existing_resource = Resources.query.filter_by(name=name).first()
        if existing_resource is None:
            resource = Resources(name=name, description=website)
            db.session.add(resource)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'Error adding resource: {e}')

resource1 = Resources(name='Mind side by side', description='https://sidebyside.mind.org.uk')
review1 = Reviews(rating=3, content='An interesting community, but the content is a bit boring.', parent_resource=resource1)
resource2 = Resources(name='Samaritans', description='https://www.samaritans.org/')
review2 = Reviews(rating=5, content='There is always someone there, although they can only give you a very limited time. Sometimes, listening to a human voice telling me that everything is ok is helpful.', parent_resource=resource2)
resource3 = Resources(name='WPF Therapy', description='https://wpf.org.uk/')
review3 = Reviews(rating=3, content='A counselor at my university used to recommend this place, it is a shame that they are permanently closed!', parent_resource=resource3)
resource4 = Resources(name='IESO Online talking therapy', description='https://www.iesohealth.com/')
review4 = Reviews(rating=2, content='Not very useful. Doesn\'t feel very personal.', parent_resource=resource4)
resource5 = Resources(name='Mind Anxiety/Mood Peer Support Group', description='https://www.mindincamden.org.uk/services/free-support-groups')
review5 = Reviews(rating=4, content='The session is quite structured, and the facilitators are well-prepared. Can actually learn something from the one hour session online.', parent_resource=resource5)
with app.app_context():
    db.session.add(resource2,review2)
    db.session.add(resource3,review3)
    db.session.add(resource4,review4)
    db.session.add(resource5,review5)
    db.session.commit()

# # search on https://www.nhs.uk/service-search/mental-health/find-an-urgent-mental-health-helpline/result?Latitude=51.52532527480014&Longitude=-0.1307660796246909&Answer=yes&Age=18
# # from geopy.geocoders import Nominatim
#
# # def get_lat_long(postcode):
# #     geolocator = Nominatim(user_agent="geoapiExercises")
# #     location = geolocator.geocode(postcode)
# #     if location:
# #         return location.latitude, location.longitude
# #     else:
# #         return None, None
# #
# # # Example usage
# # postcode = "SW1A 1AA"  # Replace with any UK postcode
# # latitude, longitude = get_lat_long(postcode)
# # print(f"Latitude: {latitude}, Longitude: {longitude}")
