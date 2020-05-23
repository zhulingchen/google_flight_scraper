# Google Flight Scraper
Lingchen Zhu's own scraper for Google Flights search and result compilation written in Python. It is designed for my personal and convenient use only, not for any commercial purposes.

## Dependencies
### WebDriver
You must download either [ChromeDriver](https://chromedriver.chromium.org/downloads) or [GeckoDriver](https://github.com/mozilla/geckodriver/releases/) (for Firefox) before using such application.

### Python packages
- [numpy](https://www.numpy.org)
- [pandas](https://pandas.pydata.org/)
- [selenium](https://selenium-python.readthedocs.io/)

## Usage
main.py [-h] [-a airports airports] [-d dates [dates ...]] [-l checklist]

| Arguments     									  | Description                                      |
| :---          									  | :---                                             |
| -h, --help                                          | show this help message and exit 				 |
| -a airports airports, --airports airports airports  | depart and arrival airports 					 |
| -d dates [dates ...], --dates dates [dates ...]     | depart and return dates 						 |
| -l checklist, --checklist checklist                 | checklist file including many airports and dates |

Note: if -l/--checklist is used, -a/--airports and -d/--dates will be overridden.