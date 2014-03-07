from bs4 import BeautifulSoup, NavigableString
import urllib2
import simplejson

def retrieve_states(soup):
	'''Return a list of states given an html file'''
	first_table = soup.table
	states = []
	for n in first_table.find_all('a'):
		curr_city = n.string

		states.append(replace_space(curr_city,'states'))	
	
	return states

def retrieve_cities(state):
	html = "http://www.mystore411.com/store/list_state/3/" + state + "/Walmart-store-locations"	
	content = urllib2.urlopen(html).read()
	soup = BeautifulSoup(content)

	html2 = "http://www.mystore411.com/store/list_state/3/" + state + "/Walmart-store-locations?page=2&"	
	content2 = urllib2.urlopen(html2).read()
	soup2 = BeautifulSoup(content2)

	first_table = soup.table
	cities = []
	for n in first_table.find_all('a'):
		if n.parent.name == 'td':	
			cities.append(replace_space(n.string,'cities'))
	
	second_table = soup2.table
	for n in second_table.find_all('a'):
		if n.parent.name == 'td':
			cities.append(replace_space(n.string,'cities'))

	return cities

def replace_space(s1,purpose):
	new_s1 = ''
	for n in s1:
		if n == ' ':
			if purpose == 'states':
				new_s1 += '%20'
			else:
				new_s1 += '+'
		else:
			new_s1 += n
	
	return new_s1

html = "http://www.mystore411.com/store/listing/3/Walmart-store-locations"
content = urllib2.urlopen(html).read()
soup = BeautifulSoup(content)

states_list = retrieve_states(soup)
cities = []
for n in states_list:
	if n == 'California':
		cities = retrieve_cities(n)


addresses = []
addresses_json = []
for n in cities:
	html = "http://www.mystore411.com/store/list_city/3/California/" + n + "/Walmart-store-locations"
	content = urllib2.urlopen(html).read()
	soup = BeautifulSoup(content)

	store_link = soup.find('td','dotrow')	
	store_loc = []
	for m in store_link:
		if m.name == 'a':
			html = "http://www.mystore411.com" + m['href']
			content = urllib2.urlopen(html).read()
			soup = BeautifulSoup(content)

			store_details = soup.find_all("div", class_="store-details")
			store_details = store_details[0]
			store_loc.append(store_details.p)
	
	
	for i in store_loc:
		address = i.find('br').previous_sibling
		first_br = address.next_sibling
		area = first_br.next_sibling.string
		address = address.string.strip()

		# parse area into city, state, zip
		comma = area.find(',')
		city = area[0:comma].strip()
		# comma+2 to account for whitespace
		state_and_zip = area[comma+2:len(area)]
		whitespace = state_and_zip.find(' ')
		state = state_and_zip[0:whitespace].strip()
		zipcode = state_and_zip[whitespace:len(state_and_zip)].strip()

		addresses_json.append(simplejson.dumps({'address': address, 'city': city, 'state': state, 'zip': zipcode}))
	

f = open('addresses.json','w')
simplejson.dump(n,f)
#for n in addresses_json:
#	json.dump(n,f)
#	print n

#with open('addresses.json','w') as outfile:
#	json.dump(addresses_json,outfile)	
