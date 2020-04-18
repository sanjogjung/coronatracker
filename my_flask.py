import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from flask import Flask,render_template
app = Flask(__name__) #instantiating a Flask

@app.route("/")
def home():
  source = requests.get("https://www.worldometers.info/coronavirus/").text  #retrieving html content of the given url
  soup = BeautifulSoup(source,'lxml')  #parsing the html using lxml parser
  mydivs = soup.findAll("div", {"class": "maincounter-number"}) # searching for all div tags with given class
  total_cases = mydivs[0].span.text.strip()  # getting the text and removing the extra spaces
  total_deaths = mydivs[1].span.text.strip()
  total_recovered = mydivs[2].span.text.strip()
  cases= soup.findAll("div",{"class":"number-table-main"}) # seaching for all div tags with given class
  active_cases = cases[0].text.strip() 
  closed_cases = cases[1].text.strip()
  table = soup.findAll("div",class_ ="main_table_countries_div") # find tables with given class
  tbody = table[0].tbody # taking table's body content
  rows = tbody.findAll("tr") #taking rows from the tables for each country
  rows = rows[7:] # the first 7 rows are continents so we won't conside. we will take only countries

  countries_data = [] # empty countries data
  for row in rows:
    country_data=dict() #
    #so we are going to take 8 show 8 columns in our table
    # name,totalcases,newcases,totaldeaths,newdeaths,totalrecovered,activecases,seriouscases
    #so we are using a dictionary for each country and appending it to the list
    all_data = row.text.split("\n")[1:9] # splitting the row because of new line character and taking the 8 values
    country_data["name"]=all_data[0]
    country_data["total_cases"]=all_data[1] #replacing with
    country_data["new_cases"]=all_data[2]
    country_data["total_deaths"]=all_data[3]
    country_data["new_deaths"]=all_data[4]
    country_data["total_recovered"]=all_data[5]
    country_data["active_cases"]=all_data[6]
    country_data["serious_cases"]=all_data[7]
    countries_data.append(country_data)  # appending the country_data to the countries_data
  return render_template('index.html',countries_data=countries_data,total_cases=total_cases,total_deaths=total_deaths,total_recovered=total_recovered,active_cases=active_cases,closed_cases=closed_cases)
  # rendering the templating by passing the essential data to be shown in the html
if __name__=="__main__":
  app.run(debug=True)
                      
