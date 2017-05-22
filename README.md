# Beeradvocate Scraper
Scrape all beers from [styles page](https://www.beeradvocate.com/beer/style/).


## Installation
Run `pip install -r requirements.txt`.


## Spider
### beer
Get info from beer product page.
```
BeerItem(
    name=name,
    ba_score=ba_score,
    ba_ratings=ba_ratings,
    picture=picture,
    producer=producer,
    city=city,
    country=country,
    website=website,
    style=style,
    style_id=style_id,
    alcohol=alcohol
)
```