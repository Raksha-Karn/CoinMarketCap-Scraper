import os
import schedule
import time


def run_scrapy_spider():
    os.system("scrapy crawl coinspider")
    print("Coin spider is running, Press Ctrl+C to stop")


def schedule_scrapy_spider():
    schedule.every(1).minutes.do(run_scrapy_spider)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    print("Starting scrapy spider")
    os.system("scrapy crawl coinspider")
    schedule_scrapy_spider()
