Web Scraping and Visualization System for Cryptocurrency Prices
================================================================

Author: Stephen Moorcroft  
Date: 18/04/2025  
Version: 1.0  
GitHub: https://github.com/codemasternot/Web-scraping

Description:
------------
This project implements a Python-based system for scraping live cryptocurrency data (Bitcoin, Ethereum, and XRP) from CoinMarketCap. 
The scraped price data is stored in HDF5 format and visualized using Matplotlib to show real-time trends over time. 

The system is fully automated and supports scheduled scraping at user-defined intervals (e.g., every hour or once daily).
Visualizations are saved as PNG files for each asset and source combination.

Features:
---------
- Scrapes real-time data for BTC, ETH, and XRP from CoinMarketCap.
- Stores data in HDF5 format using h5py for efficient time-series access.
- Creates timestamped groups and stores price metadata.
- Generates visualizations using Matplotlib for each tracked asset.
- Supports flexible scheduling using the `schedule` library.
- Can run continuously as a local script.

Dependencies:
-------------
- Python 3.8+
- requests
- BeautifulSoup4
- pandas
- h5py
- matplotlib
- schedule
- csv
- os
- datetime

How to Use:
-----------
1. Install dependencies using pip:
   pip install requests beautifulsoup4 pandas h5py matplotlib schedule

2. Run the main script:
   python web_scraper.py

3. The script will:
   - Create a config file if it doesn't exist.
   - Scrape data immediately and then continue at scheduled intervals.
   - Save the data in `crypto_data/crypto_prices.h5`
   - Generate time-series PNG graphs in the `visualizations/` folder.

4. To modify scraping frequency, adjust the `schedule.every()` call near the bottom of the script.

Data Sources:
-------------
All data is sourced from public CoinMarketCap pages:
- Bitcoin: https://coinmarketcap.com/currencies/bitcoin/
- Ethereum: https://coinmarketcap.com/currencies/ethereum/
- XRP: https://coinmarketcap.com/currencies/xrp/

License:
--------
(c) 2025 Stephen Moorcroft

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, and/or sublicense.

Disclaimer:
-----------
This project is for educational purposes only. Always review a website's terms of service and `robots.txt` before scraping.
