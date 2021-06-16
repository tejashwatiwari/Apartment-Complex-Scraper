import requests
import bs4 as bs
import math
import csv

# add cf_clearnace cookie here from brwoser local storage
cookie = "37bda886f212ff4a3c45b9f63eae79e70bccdba6-1623604635-0-250"
baseUrl = "https://www.apartmentguide.com"

# url = "https://www.apartmentguide.com/apartments/California/American-Career-College-Los-Angeles/"
url = input("Enter URL of College")
inputFileName = input("Enter filename to be saved")

payload={}
headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
  'cookie': 'cf_clearance='+cookie+';'
}

response = requests.request("GET", url, headers=headers, data=payload)
soup = bs.BeautifulSoup(response.text,'lxml')

totalPages = math.ceil(int(soup.select('span[data-tid="pagination-total"]')[0].text)/20)

fields = ['name', 'phone', 'listingLink', 'managementLink', 'propertyLink']
filename = inputFileName + ".csv"
print('\nResults will be written to the file : ' + filename)
print('Total Pages: ' + str(totalPages) + '\t Total Listings: ' + soup.select('span[data-tid="pagination-total"]')[0].text )
isCSVHeader = False

for pageNumber in range(1,totalPages+1):
    result = []
    print('\nScraping Page : '+ str(pageNumber)+'/'+str(totalPages))
    response = requests.request("GET", url+'?page='+str(pageNumber), headers=headers, data=payload)
    pageSoup = bs.BeautifulSoup(response.text,'lxml')
    allListings = pageSoup.select('div[data-tid="listing-grid"] div[data-tid="standard-listing"]')

    for index, listing in enumerate(allListings):
        temp = {}
        print('\t-- Page : '+ str(pageNumber) + ' -- listing : ' + str(index+1))
        temp['name'] = listing.select('div[data-tid="property-title"]')[0].text
        temp['phone'] = listing.select('a[data-tid="property-phonenumber"]')[0].text
        temp['listingLink'] = baseUrl + listing.select('div[data-tid="listing-info"] > a')[0]['href']

#         scraping inidividual
        listingResponse = requests.request("GET", temp['listingLink'], headers=headers, data=payload)
        listingSoup = bs.BeautifulSoup(listingResponse.text,'lxml')

        try:
            temp['managementLink'] = listingSoup.select("a[data-tid='management-company-website']")[0]['href']
        except:
            pass

        try:
            temp['propertyLink'] = listingSoup.select('a[data-tid="helpful-property-website"]')[0]['href']
        except:
            pass

        result.append(temp)

    with open(filename, 'a',newline='') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        if not isCSVHeader:
            # writing headers (field names)
            writer.writeheader()
            isCSVHeader = True

        # writing data rows
        writer.writerows(result)
