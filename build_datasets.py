import urllib
import csv
import pandas as pd
from bs4 import BeautifulSoup


def check_player(url):
    if check_position(url) and check_years(url):
        print('Player: Pass')
        return True
    else:
        print('Player: Fail')
        return False


def check_position(url):
    with urllib.request.urlopen(url) as player_page:
        soup = BeautifulSoup(player_page, 'lxml')

    try:
        position = soup.find(string='Positions:').find_next(string=True)
    except:
        AttributeError

    try:
        position = soup.find(string='Position:').find_next(string=True)
    except:
        AttributeError

    #print(position)

    if 'Pitcher' in position:
        print('Position: Fail (Pitcher)')
        return False
    else:
        print('Position: Pass (Position Player)')
        return True


def check_years(url):

    start = pd.read_html(url)
    df = start[0]
    df = df.drop(df.index[len(df) - 1])
    last_year = df['Year'].dropna().astype(int).unique().max()

    # print(last_year)

    if 1980 <= last_year <=2010:
        print('Year: Pass')
        return True
    else:
        print('Year: Fail')
        return False


def get_career_numbers(player_url):
    with urllib.request.urlopen(player_url) as player_page:
        soup = BeautifulSoup(player_page, 'lxml')

    career_numbers = []
    name = soup.find('h1').get_text()
    career_numbers.append(name)

    career1 = soup.find('div', class_='p1')
    group1 = career1.find_all('p')
    for i in enumerate(group1):
        career_numbers.append((float(i[1].get_text())))

    career2 = soup.find('div', class_='p2')
    group2 = career2.find_all('p')
    for i in enumerate(group2):
        career_numbers.append((float(i[1].get_text())))

    career3 = soup.find('div', class_='p3')
    group3 = career3.find_all('p')
    for i in enumerate(group3):
        career_numbers.append((float(i[1].get_text())))

    columns = ['Name', 'WAR', 'At Bats', 'Runs', 'Hits', 'Batting Avg', 'HR', 'RBI',
               'SB', 'OBP', 'SLG', 'OPS', 'OPS+']

    player_dict = dict(zip(columns, career_numbers))

    return player_dict


def build_dataset_columns():

    columns = ['Name', 'WAR', 'At Bats', 'Runs', 'Hits', 'Batting Avg', 'HR', 'RBI',
               'SB', 'OBP', 'SLG', 'OPS', 'OPS+']

    with open('position_players.csv', 'w') as csvfile:
        dataset_writer = csv.writer(csvfile)
        dataset_writer.writerow(columns)


def add_to_dataset(player_dictionary, position):
    if position == 'Pitcher':
        file = 'pitchers.csv'
    else:
        file = 'position_players.csv'

    with open(file, 'a') as f:
        dataset_writer = csv.writer(f)
        dataset_writer.writerow(player_dictionary.values())

    return

#url = 'https://www.baseball-reference.com/players/c/colonba01.shtml' #pitcher, Bartolo Colon
#url = "https://www.baseball-reference.com/players/a/aaronha01.shtml" #position player, Hank Aaron
url = 'https://www.baseball-reference.com/players/b/biggicr01.shtml' #position player, Craig Biggio

#check_position(url)
#check_years(url)
#get_career_numbers(url)

#dict = {'Name': 'Hank Aaron', 'WAR': 143.0, 'At Bats': 12364.0, 'Runs': 2174.0, 'Hits': 3771.0, 'Batting Avg': 0.305, 'HR': 755.0, 'RBI': 2297.0, 'SB': 240.0, 'OBP': 0.374, 'SLG': 0.555, 'OPS': 0.928, 'OPS+': 155.0}

#build_dataset_columns()
#add_to_dataset(dict, 'Outfielder')