import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup


def scrape_website(website):
    print("Launching Chrome Browser...")

    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page Loaded...")
        html = driver.page_source
        time.sleep(10)

        return html
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return[
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

# This ^^^ code is all you need to continue scraping, but certain websites may start blocking or requiring
# captcha to continue. To circumvent this, you can use brightdata and use the following steps:
# make account --> go to dashboard --> proxies and scraping --> add scraping browser (this will solve 
# captcha's and connect to proxy network, cycling through different IP's.)
# this makes it so we dont have to do any of the scraping from our own device/network and instead use a
# remote browser instance in the cloud
# go to check out code and integration examples -- this will show you what code to use based on language
# and library.
# This would be the code to use instead:
#
# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from bs4 import BeautifulSoup
#
# SBR_WEBDRIVER = 'https://brd-customerhl_8a10678a-zone-ai_scraper:td7ei0kyeqq1@brd.superproxy.io:9515'
# 
# def scrape_website(website):
#    print(Connecting to Scraping Browser...')
#
#    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
#    with Remote(sbr_connection, options=ChromeOptions()) as driver
#       driver.get(website)
## Captcha handling code(use this if expecting CAPTCHA on the target page):
#       print('Waiting for captcha to solve...')
#       solve_res = driver.execute('executeCdpCommand', {
#           'cmd': 'Captcha.waitForSolve',
#           'params': {'detectTimeout': 10000},
#       })
#       print('Captcha solve status:', solve_res['value']['status'])
#       print('Navigated! Scraping page content...')
#       html = driver.page_source
#       return html