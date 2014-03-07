from bs4 import BeautifulSoup
import urllib2
import json
import sys

def median_incomes():
	html = 'http://en.wikipedia.org/wiki/California_locations_by_income'
	content = urllib2.urlopen(html).read()
	soup = BeautifulSoup(content)

	first_table = soup.find_all('table', limit=2)	
	first_table = first_table[1]
	each_row = first_table.find_all('td')

	data = []
	data2 = {}
	num_entries = 58

	# first td = name, third td = household median income
	for n in range(0,num_entries):
		county = each_row[n*5].getText() + ' County'
		income = each_row[n*5+3].getText()
		print county
		# remove dollar sign and commas from median income
		income = remove(income)
		data2.update({county:income})
		print data2
#	print data2
	return data2

def remove(income):
	# remove dollar sign
	income = income[1:]
	# remove commas and put each in list
	income = income.split(',')
	income = int(''.join(income))
	return income

incomes = median_incomes()
f = open('median_income.json','w')
json.dump(incomes,f,indent=4)

#largest = 0
#smallest = sys.maxint
#for n in incomes:
#	if largest < n['county']:
#		largest = n['county']
#	if smallest > n['county']:
#		smallest = n['county']
#
#print "Smallest: " + str(smallest)
#print "Largest: " + str(largest)
