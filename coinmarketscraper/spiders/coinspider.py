import scrapy
import datetime
import pytz
from ..agents import get_random_user_agent
from ..supabase_client import supabase


class CoinspiderSpider(scrapy.Spider):
    name = "coinspider"
    coins = []
    custom_settings = {
        'USER_AGENT': get_random_user_agent(),
    }

    def start_requests(self):
        search_url = "https://coinmarketcap.com/"
        yield scrapy.Request(search_url, callback=self.discover_coins, meta={'url': search_url})

    def discover_coins(self, response):
        coin_urls = response.css('div.sc-4c05d6ef-0.bLqliP a.cmc-link::attr(href)').extract()
        self.logger.info(f"Found {len(coin_urls)} coins")
        for url in coin_urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_coin)

    def parse_coin(self, response):
        coin_icon = response.css('div[data-role="coin-logo"] img::attr(src)').extract_first() or 'N/A'
        coin_name = response.css('span[data-role="coin-name"]::text').extract_first() or 'N/A'
        coin_code = response.css('span[data-role="coin-symbol"]::text').extract_first() or 'N/A'
        coin_rank = response.css('h1.sc-65e7f566-0.hIeodp div.BasePopover_base__T5yOf.popover-base div[data-role="chip-content-item"] span::text').extract_first()
        coin_price_usd = response.css('div.sc-65e7f566-0.czwNaM.flexStart.alignBaseline span::text').extract_first() or 'N/A'
        coin_market_cap_usd = response.css('div.StatsInfoBox_base__kP2xM dd.sc-65e7f566-0.eQBACe.StatsInfoBox_content-wrapper__onk_o div.CoinMetrics_sib-content-wrapper__E8lu8 div.CoinMetrics_overflow-content__tlFu7 div.BasePopover_base__T5yOf.popover-base span::text').extract()
        coin_up_or_down = response.css('div.sc-65e7f566-0.eQBACe div.sc-4c05d6ef-0.sc-c0738578-0.dlQYLv.fwBchk p::text').extract()
        coin_color = response.css('div.sc-65e7f566-0.eQBACe div.sc-4c05d6ef-0.sc-c0738578-0.dlQYLv.fwBchk p::attr(color)').extract_first()
        coin_website_url = response.css('a[data-test="chip-website-link"]::attr(href)').extract()
        coin_rating = response.css('div.RatingSection_wrapper__T_YeR span::text').extract_first()

        self.logger.info(f"Found {coin_name}")

        item = {
            'icon': coin_icon,
            'name': coin_name,
            'code': coin_code,
            'rank': int(coin_rank.split('#')[1]) if coin_rank else 'N/A',
            'price_usd': coin_price_usd,
            'market_cap_usd': coin_market_cap_usd[0] if coin_market_cap_usd else 'N/A',
            'up_or_down': f"+{coin_up_or_down[0]}" if coin_color != "red" else f"-{coin_up_or_down[0]}",
            'website_url': coin_website_url[0].split('/')[2] if coin_website_url else 'N/A',
            'rating': float(coin_rating) if coin_rating else 0.0,
            'url': response.url,
            'updated_at': datetime.datetime.now(pytz.utc).isoformat(),
        }

        self.coins.append(item)

    def close(self, reason):
        self.logger.info(f"Fetched {len(self.coins)} coins")

        try:
            self.logger.info("Inserting into supabase")
            response = supabase.table("coins").upsert(self.coins, on_conflict="code").execute()
            self.logger.info(f"Inserted {len(self.coins)} coins into Supabase")
        except Exception as exception:
            self.logger.error(f"Error inserting into Supabase: {exception}")
