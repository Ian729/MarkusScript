import requests
import bs4, csv
import os
import filecmp

# new Session()
s = requests.Session()
# constants
subject1 = "csc411-2018-09"
subject2 = "csc418-2018-09"
subject3 = "csc458-2018-09"
user_login = input("username:")
user_password = input("password:")
for subject in [subject1, subject2, subject3]:
	markus_url = 'https://markus.teach.cs.toronto.edu/'+subject+'/?locale=en'
	#send post request
	response = s.post(markus_url, data = {'user_login':user_login, 'user_password':user_password})
	#parse HTML
	page_soup = bs4.BeautifulSoup(response.text,'html.parser')
	#find the table we want
	table = page_soup.find('table')
	
	file_exist = os.path.isfile(subject+".csv") 
	#open a csv file to write
	if file_exist:
		f = open(subject+"2.csv","w")
	else:
		f = open(subject+".csv","w")
	#write header
	f.write("NAME, RESULTS\n")
	#find all rows
	all_tr =  table.findAll('tr')
	for tr in all_tr:
		#find the table cells in current row
		all_td = tr.findAll('td')
		if all_td:
			name = all_td[0].a.text.strip()
			print(name,end="\t")
			if all_td[2].p:
				result = all_td[2].p.text.replace(" ","").replace("\n","")+"\n"
				print(result)
			else:
				result = all_td[2].text.strip()+"\n"
				print(result)
			f.write(",".join((name, result)))
	f.close()
	if file_exist:
		if filecmp.cmp(subject+".csv", subject+"2.csv"):
			#no update recently
			os.remove(subject+"2.csv")
		else:
			#replace the original file
			os.rename(subject+"2.csv",subject+".csv")
			# and send message
			