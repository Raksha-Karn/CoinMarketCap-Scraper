
# CoinSpider

CoinSpider is a Scrapy-based web scraper designed to collect cryptocurrency data from CoinMarketCap. It gathers essential information about coins, including their icon, name, symbol, rank, price, market capitalization, rating, and more. The scraper then stores the data in a Supabase database for further analysis.

## Features

- Scrapes data from CoinMarketCap.
- Extracts details such as coin name, symbol, rank, price, market cap, and more.
- Stores data in Supabase using `upsert` functionality.
- Handles missing data gracefully and logs the scraping process.
- Includes a random user-agent for anonymity.

## Installation

### Prerequisites

- Python 3.7+
- Supabase account (for storing scraped data)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/coinscraper.git
   cd coinscraper
2. Install the requirements: 
`` pip install -r requirements.txt``

3. Run the spider:
``scrapy crawl coinspider`` 

