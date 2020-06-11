import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpider(scrapy.Spider):
    name='coin'
    allowed_domains=['https://www.livecoin.net/en']
    start_urls=['https://www.livecoin.net/en']
    def __init__(self):
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.set_window_size(1920,1080)#setting the viewPort to maximum
        driver.get("https://www.livecoin.net/en")

        tab=driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        tab[4].click()

        self.html=driver.page_source #this is a string not a selector object
        driver.close()

        #cannot specify the callback method in selenium, as a solution make a fake request to the website and in parse method instead of parsing the response we get we use self.html. But self.html is a string not a selector object, for that import Selector class from scrapy.selector

    def parse(self,response):
        modResponse=Selector(text=self.html)#now it is a selctor object and xpath exp can be used against it
        currencies=modResponse.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]")
        for currency in currencies:
            yield{
                'currency_pair':currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)':currency.xpath(".//div[2]/span/text()").get()
            }
        #item scraped count may sometimes be less than what is actually on the page, because  website fits the content browser resolution. So we need to fit the viewPort to maximum resolution
