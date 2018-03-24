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


def check_hof(name):
    hof_pd = pd.read_html('https://www.baseball-reference.com/awards/hof.shtml')
    hof_list = hof_pd[0]
    hof_names = hof_list['Name']

    if name in list(hof_names):
        return 1
    else:
        return 0


def get_career_numbers(player_url):
    with urllib.request.urlopen(player_url) as player_page:
        soup = BeautifulSoup(player_page, 'lxml')

    career_numbers = []
    name = soup.find('h1').get_text()
    career_numbers.append(name)

    career1 = soup.find('div', class_='p1')
    group1 = career1.find_all('p')
    for i in enumerate(group1):
        if len(group1) == 5:
            career_numbers.append((float(i[1].get_text())))
        else:
            if i[0] % 2 == 0:
                pass
            else:
                career_numbers.append((float(i[1].get_text())))

    career2 = soup.find('div', class_='p2')
    group2 = career2.find_all('p')
    for i in enumerate(group2):
        if len(group2) == 3:
            career_numbers.append((float(i[1].get_text())))
        else:
            if i[0] % 2 == 0:
                pass
            else:
                career_numbers.append(float(i[1].get_text()))

    career3 = soup.find('div', class_='p3')
    group3 = career3.find_all('p')
    for i in enumerate(group3):
        if len(group3) == 4:
            career_numbers.append((float(i[1].get_text())))
        else:
            if i[0] % 2 == 0:
                pass
            else:
                career_numbers.append((float(i[1].get_text())))

    career_numbers.append(check_hof(name))

    columns = ['Name', 'WAR', 'At Bats', 'Runs', 'Hits', 'Batting Avg', 'HR', 'RBI',
               'SB', 'OBP', 'SLG', 'OPS', 'OPS+','HOF']

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



