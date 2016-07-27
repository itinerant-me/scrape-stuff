#this program scrapes github for ready to hire candidates AS OF TODAY
from selenium import webdriver
import xlsxwriter
import time
import re

master_dictionary = {'githublink': '', 'imageurl': '', 'email': '',
                    'REPOSITORIES': '', 'GISTS': '', 'FOLLOWERS': ''}
master_array = []

whattosearch = input("Enter keywords: ")
wheretosearch = input("Enter Location: ")
howmanypagestosearch = input("Enter how many pages to search: ")
githublogin = input("Enter Github login: ")
githubpass = input("Enter Github password: ")
totalpages = int(howmanypagestosearch)
driver = webdriver.Chrome()
driver.get("http://www.octohunt.com")
time.sleep(2)
driver.refresh()
driver.find_element_by_xpath('/html/body/div[1]/i').click()
time.sleep(6)
driver.find_element_by_xpath('//*[@id="login_field"]').send_keys(githublogin)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(githubpass)
driver.find_element_by_xpath('//*[@id="login"]/form/div[3]/input[3]').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="skills"]').send_keys(whattosearch)
driver.find_element_by_xpath('//*[@id="location"]').send_keys(wheretosearch)
driver.find_element_by_xpath('//*[@id="search"]/i').click()
time.sleep(3)
for i in range(1, totalpages):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(6)

html_source = driver.page_source
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_source,"html.parser")
countelements = 1

workbook = xlsxwriter.Workbook('DRIVE:\\XXXX\\XXXX\\XXXXX\\collected_data.xlsx')
#configure your drive download path here
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A', 30)
worksheet.set_column('B:B', 30)
worksheet.set_column('C:C', 30)
worksheet.set_column('D:D', 15)
worksheet.set_column('E:E', 15)
worksheet.set_column('F:F', 15)

bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Github Link', bold)
worksheet.write('B1', 'Image Link', bold)
worksheet.write('C1', 'Email Id', bold)
worksheet.write('D1', 'Repositories', bold)
worksheet.write('E1', 'GISTS', bold)
worksheet.write('F1', 'Followers',bold)

startcount = 2
columnA = 'A'
columnB = 'B'
columnC = 'C'
columnD = 'D'
columnE = 'E'
columnF = 'F'

for x in soup.find_all('div', {'class': 'ui segment result'}):
    master_dictionary = {}
    for each_div in x.find_all('div', {'class': 'ui right corner mini label hire mobile'}):
        countelements+=1
        githublink = str(each_div.nextSibling.attrs.get('href'))
        followerscount = githublink + str("/followers")
        repositoriescount = githublink + str("/repositories")
        #print(githublink)
        master_dictionary['githublink']=githublink
        string1 = githublink
        element1 = columnA + str(startcount)
        worksheet.write(element1, string1)

        #print(followerscount)
        #print(repositoriescount)
        imagelink = str(each_div.nextSibling.next.attrs.get('src'))
        #print(imagelink)
        master_dictionary['imageurl'] =imagelink
        string2 = imagelink
        element2 = columnB + str(startcount)
        worksheet.write(element2, string2)

        y = len(x.find_all('a', {"class": "ui compact small icon button mobile"}))
        z = x.find_all('a', {"class": "ui compact small icon button mobile"})[y - 1]
        email = str(z)
        if "mailto:" in email:
            match = re.search(r'[\w\.-]+@[\w\.-]+', email)
            emailink = str(match.group(0))
            #print(emailink)
            master_dictionary['email'] = emailink
            string3 = emailink
            element3 = columnC + str(startcount)
            worksheet.write(element3, string3)

        else:
            emailink = "email not found"
            #print(emailink)
            string3 = emailink
            master_dictionary['email'] = "NULL"
            element3 = columnC + str(startcount)
            worksheet.write(element3, string3)

        valuebar = x.find_all('div', {'class': 'value'})
        for i in range (0,3): #for i in range (0,len(valuebar)):
            if i==0:
                displaytext = "REPOSITORIES : "
                dataelement = str(valuebar[i])
                matchedelement = re.findall(r'\b\d+\b', dataelement)
                strip1 = str(matchedelement).strip('[]')
                finaldata = int(str(strip1).strip("'"))
                repocount = finaldata
                master_dictionary['REPOSITORIES'] = repocount
                #print(displaytext + str(repocount))
                string4 = repocount
                element4 = columnD + str(startcount)
                worksheet.write(element4, string4)

            if i==1:
                displaytext = "GISTS : "
                dataelement = str(valuebar[i])
                matchedelement = re.findall(r'\b\d+\b', dataelement)
                strip1 = str(matchedelement).strip('[]')
                finaldata = int(str(strip1).strip("'"))
                gistcount = finaldata
                master_dictionary['GISTS'] = gistcount
                #print(displaytext + str(gistcount))
                string5 = gistcount
                element5 = columnE + str(startcount)
                worksheet.write(element5, string5)

            if i==2:
                displaytext = "FOLLOWERS : "
                dataelement = str(valuebar[i])
                matchedelement = re.findall(r'\b\d+\b', dataelement)
                strip1 = str(matchedelement).strip('[]')
                finaldata = int(str(strip1).strip("'"))
                followcount = finaldata
                master_dictionary['FOLLOWERS'] = followcount
                #print(displaytext + str(followcount))
                string6 = followcount
                element6 = columnF + str(startcount)
                worksheet.write(element6, string6)
                startcount+=1
        master_array.append(master_dictionary)
#print("total results found:" + str(countelements))
#print("total printed elements:"+str(startcount-1))
#print(master_array)
#print(len(master_array))

workbook.close()
