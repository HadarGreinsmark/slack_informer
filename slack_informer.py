#!/usr/bin/env python3

import os
from datetime import date, timedelta
from slacker import Slacker
import scrapy
from scrapy.crawler import CrawlerProcess

SLACK_CHANNEL = '#mat'

tomorrow = date.today() + timedelta(days=1)

def main():
    if tomorrow.weekday() > 4:
        raise "Can only get menus from Monday to Friday."

    process = CrawlerProcess()

    process.crawl(HorsSpider)
    process.start()


def slack_notify(token, label, menu):
    slack = Slacker(token)
    slack.chat.post_message(SLACK_CHANNEL, '*' + label + '*\n>>>' + menu + '')


class HorsSpider(scrapy.Spider):
    name = 'HorsSpider'
    url = 'http://www.hors.se/veckans-meny/?week_for=' + tomorrow.isoformat()
    start_urls = [url]

    def parse(self, response: scrapy.http.Response):
        table_rows = response.xpath('(//table[@id="mattabellen"])[1]//tr[position()>1]')
        row = table_rows[tomorrow.weekday()]
        label = row.xpath('th/text()').extract()[0]
        menu = ''.join(row.xpath('td/text()').extract())
        slack_notify(os.environ['SLACK_TOKEN'], label, menu)


if __name__ == '__main__':
    main()
