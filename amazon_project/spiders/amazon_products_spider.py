import scrapy

from amazon_project.items import AmazonProjectItem


class AmazonProductSpider(scrapy.Spider):
    name = "amazon"
    start_urls = [
        'https://www.amazon.com/s?i=specialty-aps&bbn=16225011011&rh=n%3A%2116225011011%2Cn%3A10802561&ref=nav_em_T1_0_4_NaN_15__nav_desktop_sa_intl_cleaning_supplies'
    ]

    def parse(self, response):
        items = response.css(
            'div.a-section.a-spacing-none.a-spacing-top-small h2 a.a-link-normal.a-text-normal::attr(href)').getall()

        for item in items:
            yield response.follow(item, callback=self.parse_details)

        # follow pagination link
        next_page = response.css('div.a-text-center ul.a-pagination li.a-last a::attr(href)').get()
        if next_page is not None and next_page[-1] != '3':
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_details(self, response):
        product = AmazonProjectItem()
        product['name'] = response.css('div.a-section.a-spacing-none h1 span::text').get().strip()
        product['url'] = response.request.url.split('ref')[0]
        product['image_url'] = response.css('div.imgTagWrapper img::attr(data-old-hires)').get()
        product['price'] = response.css(
            'div.a-section.a-spacing-small td.a-span12 span.a-size-medium.a-color-price.priceBlockBuyingPriceString::text').get()

        if not product['price']:
            product['price'] = 'null'
        else:
            product['price'] = float(product['price'].strip('$'))

        return product
