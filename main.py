from bs4 import BeautifulSoup as bs
import lxml
import pandas as pd
import numpy as np
import requests

link_list = []
column=[]
combined_df = pd.DataFrame()
date = ''
location = ''
scores=[]
#Finding the maximum amount of pages for us to iterate through
def maxpage():
  page = requests.get('https://www.dci.org/scores')
  soup = bs(page.text, 'lxml')
  pagination_div = soup.find('div', {'class': 'pagination'})

  if pagination_div:
      total_span = pagination_div.find('span', {'class': 'total'})
      if total_span:
        total_value = int(total_span.text)
        print(f"Total Pages: {total_value}. Webscrape will begin momentarily")
        return total_value
      else:
          print("Total span not found")
  else:
      print("Pagination div not found")

max_page = maxpage()

#Iterating through each page of the website. link_list is all of the links to each score page. There are multiple links on each page, so the links are grouped by each page and referenced later by variables j and k.
url = 'https://www.dci.org/scores?page='
for i in range(0, max_page+1):
    req = requests.get(url+str(i))
    soup = bs(req.text, 'lxml')
    box = soup.find('div', {'class': 'scores-table scores-listing'})
    links = [link['href'] for link in box.find_all('a', href=True)]
    link_list.append(links)
    print(f"{round((i/max_page*100), 2)}% complete")
  
#Iterating through each website
#j is a page of links and k is each individual link on a page
for j in range (0, max_page - 1): 
  for k in range(0,len(link_list[j])-1):
    corps_names = []
    
    url2 = (f'https://www.dci.org{link_list[j][k]}')
    url3 = url2.replace('final-scores','recap')
    page = requests.get(url3)
    print(url3)

    #Setting up the column headers, this section will grab Corps, General Effect, Visual, Music. Will Append Date, Location, Subtotal, and Total
    soup2 = bs(page.content, 'html.parser')
    html1 = soup2.find('div', {'class': 'top sort-item'})
    html2 = html1.find('h4')
    column = [corps.text.strip().capitalize() for corps in html2]
    column.append('Date')
    column.append('Location')
    
    try:
      for i in range(1,5):
        html3 = soup2.find_all('div', {'class': 'title'})[i]
        column.append(html3.text.strip())
      
      if '' in column:
        column.remove('')
      
      if 'Penalties' in column:
        column.remove('Penalties')
      
      if 'Timing & Penalties' in column:
        column.remove('Timing & Penalties')
      
      column.append('Subtotal')
      column.append("Total")
    
    except:
      print("Something weird happened with the columns")
      continue
      
    #Pulls the names of the particular corps performing on that competition
    html4 = soup2.find('div', {'class': 'sticky-corps'})
    corps_list = html4.find_all('ul')
    for corps in corps_list:
       corps_names.extend([name.text.strip() for name in corps.find_all('li')])

    #Pulls the total scores of each subsection General Effect, Visual, Music, Subtotal, and Total. Skips the penalties column 
    html5 = soup2.find_all('div', {'class': 'column column-total'})
    for div in html5:
      spans = div.find_all('span')
      for span in spans:
        score = span.text.strip()
        if '.' in score:
          scores.append(score)

    
  
    #Pulls the date of the performance and the location of the performance
    html6 = soup2.find('div', {'class': 'details'})
    date_element = html6.find('div').find('span')
    location_element = html6.find_all('div')[1].find('span')

    date = date_element.text.strip()
    location = location_element.text.strip()


     #Pulls elements together into comprehensive lists, setting up for pandas. Some scores in early years were not recorded and are null values noted as '---' in the columns.
    try:
      new_lists = []
      df = pd.DataFrame(columns = column)

      for i in range(len(corps_names)):
        scores_list = scores[i*5:(i+1)*5]
        comp = [corps_names[i], date, location] + scores_list
        new_lists.append(comp)
        
      df = pd.DataFrame(data=new_lists, columns=column)
      
      if combined_df.empty:
        combined_df = df
      else:
        combined_df = combined_df.merge(df, how='outer')
      pd.set_option('display.max_columns', None)
      pd.set_option('display.expand_frame_repr', False)

      print(f"Scrape Complete for {date} at {location}! Moving on to the next one!")

    except:
        print(f"Error occurred for {date} at {location}. Skipping to the next day.")
        continue
print(combined_df)

combined_df.to_csv (r'C:\Users\home\Desktop\Data Analysis\Project 1 - DCI Analysis\
export_dataframe.csv', index = None, header=True)

