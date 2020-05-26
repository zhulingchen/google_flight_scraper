# Google Flight Scraper
Lingchen Zhu's own scraper for Google Flights search and result compilation written in Python. It is designed for my personal and convenient use only, not for any commercial purposes.

## Disclaimer
The software is provided "As is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

## Dependencies
### WebDriver
You must download either [ChromeDriver](https://chromedriver.chromium.org/downloads) or [GeckoDriver](https://github.com/mozilla/geckodriver/releases/) (for Firefox) before using such application.

### Python packages
- [pandas](https://pandas.pydata.org/)
- [selenium](https://selenium-python.readthedocs.io/)

## Usage
main.py [-h] [-a airports airports] [-d dates [dates ...]] [-l checklist]

| Arguments     									                  | Description                                                                |
| :---          									                  | :---                                                                       |
| -h, --help                                                          | show this help message and exit 				                           |
| -a AIRPORT AIRPORT, --airports AIRPORT AIRPORT                      | depart and arrival airports 					                           |
| -d YYYY-MM-DD [YYYY-MM-DD ...], --dates YYYY-MM-DD [YYYY-MM-DD ...] | depart and return dates (one date for one way or two dates for round-trip) |
| -l FILE, --checklist FILE                                           | checklist file (a .csv or an Excel file) including many airports and dates |
| -n, --flight-number                                                 | get the flight number                                                      |
| -c [CARRIER [CARRIER ...]], --carriers [CARRIER [CARRIER ...]]      | filter specific carriers                                                   |
| -e [EMAIL [EMAIL ...]], --email [EMAIL [EMAIL ...]]                 | email address(es) that receive results                                     |

Note: if -l/--checklist is used, -a/--airports and -d/--dates will be overridden.

Also, please update [email_config.json](./email_config.json) with your own SMTP server and login information if you want to send results via email.