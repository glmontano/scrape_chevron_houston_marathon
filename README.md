## Chevron Houston Marathon Data Scraper

Scrapes data from 

	'https://track.rtrt.me/e/HOU-{YEAR}'

where `YEAR` is the year of the marathon of interest. Successfully tested for `2022` and `2023`.

## Prerequisites

Install the required packages. After cloning and pulling the repo, apply

`pip install -r requirements.txt`

Google Chrome driver is also required. Download the *driver version* required for your *Google Chrome browser version*.

	`https://chromedriver.chromium.org/downloads`

## To Do

Update driver functions due to `DeprecationWarning`:

```shell
 DeprecationWarning: executable_path has been deprecated, please pass in a Service object
  driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_options)
```

Explanation here: `https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python`