import os
import logging
from datetime import datetime, timedelta
from urllib.request import urlretrieve
from urllib.error import ContentTooShortError, HTTPError, URLError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

date = datetime.now()

got_file = False
attempts_no = 0

# attempt to get the file from current month and if not existent go back one month up to 12 months
while not got_file and attempts_no < 12:
    year_month = date.strftime("%Y-%m")
    
    url = f"https://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/UK-HPI-full-file-{year_month}.csv"
    
    directory = "data/source/"
    filename = f"UK-HPI-full-file-{year_month}.csv"
    dest_path = os.path.join(directory, filename)
    os.makedirs(directory, exist_ok=True)

    try:
        if os.path.exists(dest_path):
            logging.info(f"{filename} already exist")
        else:
            urlretrieve(url, dest_path)
            logging.info(f"{filename} retrieved successfuly")
        
        got_file = True

    except (ContentTooShortError, HTTPError, URLError) as e:
        logging.error(f"{filename} retrieved failed: {e}")
        # set date to previous month
        date = date.replace(day=1) - timedelta(days=1)
        attempts_no += 1


