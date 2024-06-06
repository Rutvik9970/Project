import time
import pymongo
import requests
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# MongoDB configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]
collection = db["trending_topics"]

# Selenium options with ProxyMesh configuration
chrome_options = Options()
chrome_options.add_argument('--proxy-server=http://us-ca.proxymesh.com:31280')

# Path to your chromedriver
chromedriver_path = 'C:\\Users\\ACER\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

# Initialize Selenium WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def login_twitter(username, password):
    driver.get("https://x.com/i/flow/login")
    wait = WebDriverWait(driver, 30)  # Increased timeout to 30 seconds

    try:
        print("Waiting for username input field to be present...")
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        print("Username input field found.")
        
        user_input.send_keys(username)
        user_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Adjust the sleep time if needed
        
        print("Waiting for password input field to be present...")
        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        print("Password input field found.")
        
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.RETURN)
        
        time.sleep(5)  # Wait for login to complete
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        return

def fetch_trending_topics():
    driver.get("https://x.com/explore/tabs/keyword")
    time.sleep(5)

    try:
        print("Fetching trending topics...")
        # Adjust the selector based on the actual HTML structure of the Twitter page
        trends = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now'] div span.css-1jxf684")
        trending_topics = [trend.text for trend in trends[:5]]
        print("Trending topics:", trending_topics)  # Debug print
        return trending_topics
    except Exception as e:
        print(f"Error fetching trending topics: {e}")
        driver.quit()
        return []

def save_to_mongodb(trending_topics, ip_address):
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "_id": unique_id,
        "trend1": trending_topics[0] if len(trending_topics) > 0 else "",
        "trend2": trending_topics[1] if len(trending_topics) > 1 else "",
        "trend3": trending_topics[2] if len(trending_topics) > 2 else "",
        "trend4": trending_topics[3] if len(trending_topics) > 3 else "",
        "trend5": trending_topics[4] if len(trending_topics) > 4 else "",
        "timestamp": timestamp,
        "ip_address": ip_address
    }
    
    print("Data to be saved:", data)  # Debug print
    collection.insert_one(data)
    return data

def main():
    username = "RutvikPathak14"
    password = "thedestroyer"
    
    login_twitter(username, password)
    
    trending_topics = fetch_trending_topics()
    
    response = requests.get("https://ipinfo.io")
    ip_address = response.json().get("ip", "Unknown IP")
    
    data = save_to_mongodb(trending_topics, ip_address)
    
    driver.quit()
    return data

if __name__ == "__main__":
    main()
