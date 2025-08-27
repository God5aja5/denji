import re
import asyncio
import requests
from playwright.async_api import async_playwright

# Telegram credentials
TELEGRAM_TOKEN = "7803713198:AAHNtjhBl4ecYyF3bwQZg3KG7JPv4dRiPoY"
CHAT_ID = "7265489223"

# Demo RC number (you can change this)
VEHICLE_NUMBER = "MH12AB1234"

# Your login cookies (JSON format)
COOKIES = [
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1787824873,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_clck",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "1gup526%5E2%5Efyt%5E0%5E2065"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1787829784,
        "hostOnly": False,
        "httpOnly": False,
        "name": "FCNEC",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "%5B%5B%22AKsRol9ay3_gHd_KzKLq5Bskn9v8E7Mld-M3nOxmiNoOQk1iMiKhDPfWUyVu6FB7SJwzUXUpp3WMqmmRuOB8RQxns0bmyggCzPAE_gAmWPtCmxTWqrASGjzjdbSgxxmOLLqWN7aiaQ8TE_gfcAjbLV6py4jBl4FO6Q%3D%3D%22%5D%5D"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1790853797.918949,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_KEN70KGZ0J",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "GS2.1.s1756293694$o2$g1$t1756293797$j60$l0$h1390354998"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1764064859,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_au",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "1.1.1681696966.1756288859"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1790853775.25169,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "GA1.1.1910824230.1756288859"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1756380184,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_clsk",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "qeefe5%5E1756293784483%5E3%5E1%5Ej.clarity.ms%2Fcollect"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1764069776,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_fbp",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "fb.1.1756288873881.216321712474373516"
    },
    {
        "domain": ".vehicleinfo.app",
        "expirationDate": 1790853775.243309,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_4X4MP71P5K",
        "path": "/",
        "sameSite": None,
        "secure": False,
        "session": False,
        "storeId": None,
        "value": "GS2.1.s1756293688$o2$g1$t1756293774$j32$l0$h1356398435"
    }
]

# Regex patterns for vehicle details
def extract_vehicle_details(html):
    patterns = {
        'insurance_policy_no': r'Insurance Policy No\.\s*</div>\s*<div[^>]*>([^<]+)',
        'insurance_company': r'Insurance Company\s*</div>\s*<div[^>]*>([^<]+)',
        'insurance_expiry': r'Expires On\s*([^<]+)',
        'owner_name': r'Owner Name\s*</div>\s*<div[^>]*>([^<]+)',
        'relation': r'Son/ Daughter/ Wife Of\s*</div>\s*<div[^>]*>([^<]+)',
        'ownership': r'Ownership\s*\(Serial No\.\)\s*</div>\s*<div[^>]*>([^<]+)',
        'registration_no': r'Registration No\s*</div>\s*<div[^>]*>([^<]+)',
        'registration_authority': r'Registration Authority\s*</div>\s*<div[^>]*>([^<]+)',
        'maker': r'Maker Name\s*</div>\s*<div[^>]*>([^<]+)',
        'model': r'Model Name\s*</div>\s*<div[^>]*>([^<]+)',
        'vehicle_class': r'Vehicle Class\s*</div>\s*<div[^>]*>([^<]+)',
        'fuel_type': r'Fuel Type\s*</div>\s*<div[^>]*>([^<]+)',
        'engine_no': r'Engine Number\s*</div>\s*<div[^>]*>([^<]+)',
        'chassis_no': r'Chassis Number\s*</div>\s*<div[^>]*>([^<]+)',
        'registration_date': r'Registration Date\s*</div>\s*<div[^>]*>([^<]+)',
        'vehicle_age': r'Vehicle Age\s*</div>\s*<div[^>]*>([^<]+)',
        'fitness_upto': r'Fitness Upto\s*</div>\s*<div[^>]*>([^<]+)',
        'color': r'Color\s*</div>\s*<div[^>]*>([^<]+)',
        'seat_capacity': r'Seat Capacity\s*</div>\s*<div[^>]*>([^<]+)',
        'body_type': r'Body Type\s*</div>\s*<div[^>]*>([^<]+)',
        'manufacture_date': r'Manufacture Month\s*-\s*Year\s*</div>\s*<div[^>]*>([^<]+)',
        'cylinder_capacity': r'Cylinder Capacity\s*</div>\s*<div[^>]*>([^<]+)',
        'unladen_weight': r'Unload Weight\s*</div>\s*<div[^>]*>([^<]+)'
    }

    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, html)
        if match:
            result[key] = match.group(1).strip()
    return result

async def scrape_vehicle_details(vehicle_number):
    url = f"https://vehicleinfo.app/rc-details/{vehicle_number}?rc_no={vehicle_number}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies(COOKIES)
        page = await context.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(7000)
        html = await page.content()
        await browser.close()
        return html, extract_vehicle_details(html)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

async def main():
    html, details = await scrape_vehicle_details(VEHICLE_NUMBER)

    if not details:
        send_to_telegram("❌ No details found for the given RC number.")
    else:
        send_to_telegram(f"✅ Vehicle Data for {VEHICLE_NUMBER}\n\nParsed:\n{details}\n\nRaw:\n{html[:1500]}...")

if __name__ == "__main__":
    asyncio.run(main())
