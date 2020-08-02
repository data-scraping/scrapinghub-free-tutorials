import scrapy


class LoginspiderSpider(scrapy.Spider):
    name = 'loginspider'
    allowed_domains = ['quotes.toscrape.com']
    url_login = 'http://quotes.toscrape.com/login'
    start_urls = [url_login]

    def parse(self, response):
        # Submitting Forms with Spider
        """
            Submitting POST requests with Scrapy
            Handling validation tokens
            Authenticating in a website
        """
        # extract csrf token value
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        data = {
            'csrf_token' : token,
            'username' : 'user',
            'password' : 'user',
        }
        yield scrapy.FormRequest(url=self.url_login, formdata=data, callback=self.parse_quotes)

    def parse_quotes(self, response):
        # Parse the main page after the spider loggged in
        for q in response.css('div.quote'):
            yield {
                'author_name': q.css('small.author::text').extract_first(),
                'author_url': q.css(
                    'small.author ~ a[href*="goodreads.com"]::attr(href)'
                ).extract_first()
            }