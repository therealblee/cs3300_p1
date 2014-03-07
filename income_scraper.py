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
	num_entries = 58

	# first td = name, third td = household median income
	for n in range(0,num_entries):
		county = each_row[n*5].getText() + ' County'
		med_income = each_row[n*5+3].getText()
		# remove dollar sign and commas from median income
		med_income = remove(med_income)
		info = {'county': county, 'income': med_income}
		data.append(info)
	
	return data

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

largest = 0
smallest = sys.maxint
for n in incomes:
	if largest < n['income']:
		largest = n['income']
	if smallest > n['income']:
		smallest = n['income']

print "Smallest: " + str(smallest)
print "Largest: " + str(largest)
