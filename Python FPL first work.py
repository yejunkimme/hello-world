url = 'https://fbref.com/en/comps/9/'
category = 'passing_types'
target = (url + category + '/Premier-League-Stats.htm')

import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd

soup = BeautifulSoup(requests.get(target).content, 'html.parser') #url inserted

table = BeautifulSoup(soup.select_one('#all_stats_'+category).find_next(text=lambda x: isinstance(x, Comment)), 'html.parser')
	#I don't understand this... code from here (https://stackoverflow.com/questions/62969492/web-scraping-a-page-with-multiple-tables)
	#print some information from the table to screen:

for tr in table.select('tr:has(td)'):
    tds = [td.get_text(strip=True) for td in tr.select('td')] 
    
    #Each table row is defined with a <tr> tag. Each table header is defined with a <th> tag. Each table data/cell is defined with a <td> tag.


column_headers = table.findAll('tr')[1]
column_headers = [i.getText() for i in column_headers.findAll('th')]

	#code block from (https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe)

# to check the column headers and match the length with data cell count
	#print(column_headers)
	#len(column_headers)
	#len(tds[0:])
	#print(tds)


rows = table.findAll('tr')[0:]
# Get stats from each row
player_stats = [] 
	#I don't understand this. Perhaps to change type to list?

for i in range(len(rows)):
  player_stats.append([col.getText() for col in rows[i].findAll('td')])

data = pd.DataFrame(player_stats[2:], columns=column_headers[1:])

data['Crs'] = data.Crs.astype(float)
# change possible string type to float type followed guide from here:(https://towardsdatascience.com/fantasy-premier-league-value-analysis-python-tutorial-using-the-fpl-api-8031edfe9910#28e7)

slim_data = data[['Player','90s','Pos','Squad','Crs','Int','Blocks']]

slim_data.sort_values('Crs',ascending=False).head(20)

slim_data_df=slim_data.loc[slim_data.Pos=='DF']

shortlisted_dfs = slim_data_df.sort_values('Crs',ascending=False).head(20)

print(shortlisted_dfs)
