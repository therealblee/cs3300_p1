from bs4 import BeautifulSoup
import urllib2

def median_incomes():
	html = 'http://www.city-data.com/city/California.html'
	content = urllib2.urlopen(html).read()
	soup = BeautifulSoup(content)

	url_cities = []
	# loop through all ids and get urls of cities
	for n in range(0,1153):
		print n
		row = soup.find(id=str(n))	
		link = row.td.find_next('td').find_next('a')['href']
		if not('javascript' in link):
			city_url = 'http://www.city-data.com/city/' + link
			content2 = urllib2.urlopen(city_url)
			small_soup = BeautifulSoup(content2)
			
			median = small_soup.find('b', text='Estimated median household income in 2011:')
			median = median.next_sibling.string.strip()
			paren = median.find('(');
			median = median[0:paren].strip()
			
			lat = small_soup.find('b', text='Latitude:')
			lat = lat.next_sibling.string.strip()

			lng = small_soup.find('b', text=', Longitude:')
			lng = lng.next_sibling.string.strip()

			url_cities.append((median,lat,lng))
	
	return url_cities
		


# median income, latitude, longitude
city_urls = median_incomes()

f = open('median_income.txt','w')
for (x,y,z) in city_urls:
	f.write(x.encode('utf8') + "|" + y.encode('utf8') + "|" + z.encode('utf8') + '\n')

f.close()
