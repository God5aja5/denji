import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests

# Telegram details
BOT_TOKEN = "7803713198:AAHNtjhBl4ecYyF3bwQZg3KG7JPv4dRiPoY"
CHAT_ID = "7265489223"

# URL to visit
url = "https://vehicleinfo.app/rc-details/MH12AB1234?rc_no=MH12AB1234"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)  # Wait 5 seconds

        # Get full HTML content
        html = await page.content()

        # Save HTML to file
        file_path = "vehicle_details.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Parse details with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        details = {}
        for row in soup.find_all("div", class_="flex justify-between"):
            spans = row.find_all("span")
            if len(spans) == 2:
                key = spans[0].get_text(strip=True)
                value = spans[1].get_text(strip=True)
                details[key] = value

        # Print extracted details
        print("\nExtracted Vehicle Details:")
        for k, v in details.items():
            print(f"{k}: {v}")

        # Send HTML file to Telegram
        send_to_telegram(file_path)

        await browser.close()

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as file:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": file})
    if response.status_code == 200:
        print("✅ HTML file sent to Telegram successfully!")
    else:
        print(f"❌ Failed to send file. Status: {response.status_code}, Response: {response.text}")

asyncio.run(main())
