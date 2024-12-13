from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta

def fbref_scrape(link : str):
    '''
    link in the form "https://fbref.com/en/squads/{team_id}}/{year1}-{year2}/matchlogs/c9/misc/{team_name}-Scores-and-Fixtures-Premier-League"
    '''
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for_table = soup.find("table", id="matchlogs_for")
    for_rows = for_table.find_all('tr')
    
    season_df = pd.DataFrame()

    for row in for_rows:
        cols = row.find_all('td')
        if cols != [] and row.find('th').text != "" and cols[3].text[0] == 'H': #avoid header and summary rows, only write home games
            df_row = {
                'match_date' : row.find('th').text,
                'Home' : link[65:],
                'Away' : cols[7].text,
                'result' : cols[4].text,
                'gf' : cols[5].text[:2],
                'ga' : cols[6].text[:2],
                'h_yellows' : cols[8].text,
                'a_yellows' : '', #filled using different HTML table
                'h_reds' : cols[9].text,
                'a_reds': '' #filled using different HTML table

            }
            season_df = season_df._append(df_row, ignore_index=True) #append match to season dataframe'

    against_table = soup.find("table", id="matchlogs_against")
    against_rows = against_table.find_all('tr')

    for row in against_rows:
        cols = row.find_all('td')
        if cols != [] and row.find('th').text != "" and cols[3].text[0] == 'A':
            match_date = row.find('th').text
            season_df.loc[season_df['match_date'] == match_date, 'a_yellows'] = cols[8].text
            season_df.loc[season_df['match_date'] == match_date, 'a_reds'] = cols[9].text
    
    return season_df

def prem_table_scrape(date : list):
    '''
    date (list) - [M,D,YYYY], date to retrieve the premier league table from the end of the previous day
    Returns a pandas dataframe
    '''
    month = date[0]
    day = date[1]
    year = date[2]

    #subtract one day so that the table is from the end of the previous day (reflects the table before the game is played)
    date_object = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
    previous_date = date_object - timedelta(days=1)
    #convert back to string
    previous_date_str = previous_date.strftime("%Y-%m-%d")

    #backend api for some website I found, probably not allowed to use it but they don't stop me
    #+ returns convenient json data:
    previous_date = date_object - timedelta(days=1)
    link = f"https://sports-api.prod.ps-aws.com/api/football/table/date/EPL/{previous_date_str}?division_type=total&order_by=points&order=desc"

    response = requests.get(link).json()

    teams = []
    points = []
    mp = []

    for team in response['data']:
        teams.append(team['team_name'])
        points.append(team['points'])
        mp.append(team['played'])

    return pd.DataFrame({'date':'/'.join(date),'team': teams, 'points': points, 'mp': mp})

def avg_attendance(link : str):
    '''
    link in the form "https://fbref.com/en/squads/{team_id}}/{year1}-{year2}/matchlogs/c9/misc/{team_name}-Scores-and-Fixtures-Premier-League"
    '''
    attendance = 0
    games = 0 #should always be 38 but easy enough to implement it this way
    
    #go to different page with attendance stats
    link = link.replace('misc', 'schedule').replace('Match-Logs-Premier-League','Scores-and-Fixtures-Premier-League')
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for_table = soup.find("table", id="matchlogs_for")
    for_rows = for_table.find_all('tr')

    for row in for_rows:
        cols = row.find_all('td')
        if cols != [] and row.find('th').text != "" and cols[3].text[0] == 'H': #avoid header and summary rows, only write home games
            try:
                attendance += int(cols[11].text.replace(",",""))
            except:
                pass
            try:
                attendance += int(cols[9].text.replace(",","")) #for pre-xG seasons the table is different
            except:
                attendance += 0 #COVID games
            games += 1
            year = int(row.find('th').text[2:4])

    row = {"team" : link[69:],
           "season" : f'{year-1}/{year}',
           "attendance" : int(attendance / games)
    }

    return pd.DataFrame.from_dict([row])