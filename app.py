# Install dependencies first in Replit shell:
# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright

url = "https://vehicleinfo.app/rc-details/MH12AB1234?rc_no=MH12AB1234"

with sync_playwright() as p:
    # Launch Chromium in headless mode
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Go to the URL
    page.goto(url)
    
    # Wait 5 seconds for content to load
    page.wait_for_timeout(5000)
    
    # Get the full HTML content
    html = page.content()
    
    # Print the HTML
    print(html)
    
    browser.close()
