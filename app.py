from functions.scraper import scrap_open_sea
import sys

# Scrap items * 100
scrap_x = 2

if len(sys.argv) > 1:
    try:
        if int(sys.argv[1]) >= 1:
            scrap_x = int(sys.argv[1])
    except:
        pass

print(f'Scraping {scrap_x*100} Nfts')
scrap_open_sea(scrap_x)