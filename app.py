from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# URL to visit
url = "https://vehicleinfo.app/rc-details/MH12AB1234?rc_no=MH12AB1234"

# Set Chrome options for headless mode
options = Options()
options.add_argument("--headless")  # Headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

# Start Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the URL
driver.get(url)

# Wait for page to fully load
time.sleep(5)

# Get the page source
html = driver.page_source

# Close the browser
driver.quit()

# Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Extract all details (vehicle info is inside <div> tags with labels and values)
details = {}
for row in soup.find_all("div", class_="flex justify-between"):  # These divs usually hold data pairs
    spans = row.find_all("span")
    if len(spans) == 2:
        key = spans[0].get_text(strip=True)
        value = spans[1].get_text(strip=True)
        details[key] = value

# Print all extracted details
for k, v in details.items():
    print(f"{k}: {v}")
